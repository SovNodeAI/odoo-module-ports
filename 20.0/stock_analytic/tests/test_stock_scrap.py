# Copyright (C) 2019 Open Source Integrators
# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestStockScrap(TransactionCase):
    def setUp(self):
        super().setUp()

        self.product = self.env["product.product"].create(
            {
                "name": "Test Scrap Product",
                "type": "consu",
                "is_storable": True,
                "standard_price": 1.0,
            }
        )
        self.warehouse = self.env.ref("stock.warehouse0")
        self.location = self.warehouse.lot_stock_id
        # Perpetual valuation with a valuation account on the scrap location is
        # required for the scrap move to generate an accounting entry, so the
        # analytic distribution assertions below are actually exercised.
        self.stock_valuation_account = self.env["account.account"].create(
            {
                "name": "Test Stock Valuation",
                "code": "tsv",
                "account_type": "asset_current",
                "company_ids": [Command.link(self.env.company.id)],
            }
        )
        self.scrap_account = self.env["account.account"].create(
            {
                "name": "Test Scrap Loss",
                "code": "tsl",
                "account_type": "expense",
                "company_ids": [Command.link(self.env.company.id)],
            }
        )
        self.stock_journal = self.env["account.journal"].create(
            {
                "name": "Test Stock Journal",
                "code": "TSJ",
                "type": "general",
                "company_id": self.env.company.id,
            }
        )
        self.env.company.write({"account_stock_journal_id": self.stock_journal.id})
        # Odoo 20 no longer gives products a default category, so the product is
        # explicitly put in a category carrying the perpetual valuation setup.
        self.product_category = self.env["product.category"].create(
            {
                "name": "Test Scrap Category",
                "property_valuation": "real_time",
                "property_stock_valuation_account_id": self.stock_valuation_account.id,
            }
        )
        self.product.categ_id = self.product_category
        self.env.company.scrap_location_id.valuation_account_id = self.scrap_account.id
        analytic_plan = self.env["account.analytic.plan"].create({"name": "Test Plan"})
        analytic_account = self.env["account.analytic.account"].create(
            {"name": "Test Analytic Account", "plan_id": analytic_plan.id}
        )
        self.analytic_distribution = {str(analytic_account.id): 100.0}
        self.analytic_applicability = self.env["account.analytic.applicability"].create(
            {
                "business_domain": "stock_move",
                "applicability": "optional",
                "analytic_plan_id": analytic_plan.id,
            }
        )

    def __update_qty_on_hand_product(self, product, new_qty):
        self.env["stock.quant"]._update_available_quantity(
            product, self.location, new_qty
        )

    def _create_scrap(self, analytic_distribution=False):
        # Since Odoo 20 a scrap is a stock.move flagged with `is_scrap`.
        scrap_data = {
            "is_scrap": True,
            "product_id": self.product.id,
            "quantity": 1.00,
            "uom_id": self.product.uom_id.id,
            "location_id": self.location.id,
            "location_dest_id": self.env.company.scrap_location_id.id,
            "company_id": self.env.company.id,
            "analytic_distribution": analytic_distribution or False,
        }
        return self.env["stock.move"].create(scrap_data)

    def _validate_scrap_no_error(self, scrap):
        scrap.action_scrap()
        self.assertEqual(scrap.state, "done")

    def _check_analytic_distribution_no_error(self, scrap):
        # Since Odoo 20 a scrap is a stock.move, identified by `reference`
        # (the old stock.scrap `name`). stock_account names the valuation
        # journal items "<reference> - <product name>", so search them by name
        # rather than relying on the `account_move_id` link.
        name = f"{scrap.reference} - {scrap.product_id.name}"
        acc_lines = self.env["account.move.line"].search([("name", "=", name)])
        self.assertTrue(acc_lines, "No accounting entry lines for the scrap")
        for acc_line in acc_lines:
            if (
                acc_line.account_id
                != scrap.product_id.categ_id.property_stock_valuation_account_id
            ):
                self.assertEqual(
                    acc_line.analytic_distribution, scrap.analytic_distribution
                )

    def test_scrap_without_analytic_optional(self):
        self.__update_qty_on_hand_product(self.product, 1)
        scrap = self._create_scrap()
        self._validate_scrap_no_error(scrap)

    def test_scrap_without_analytic_mandatory(self):
        self.analytic_applicability.write({"applicability": "mandatory"})
        self.__update_qty_on_hand_product(self.product, 1)
        scrap = self._create_scrap()
        with self.assertRaises(ValidationError):
            self._validate_scrap_no_error(scrap)

    def test_scrap_with_analytic(self):
        self.__update_qty_on_hand_product(self.product, 1)
        scrap = self._create_scrap(
            self.analytic_distribution,
        )
        self._validate_scrap_no_error(scrap)
        self._check_analytic_distribution_no_error(scrap)
