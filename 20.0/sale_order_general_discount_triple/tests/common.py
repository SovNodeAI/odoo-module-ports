# Copyright 2026 Studio73 - Pablo Cortés <pablo.cortes@studio73.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command, models

from odoo.addons.base.tests.common import BaseCommon


class SaleOrderGeneralDiscountTripleCommon(BaseCommon):
    # Odoo 20 runs BaseCommon tests as a restricted test user: grant the
    # groups the module's scenarios need (sales, products and contacts).
    _test_user_groups = (
        "base.group_partner_manager",
        "product.group_product_manager",
        "sales_team.group_sale_salesman",
        "sale.group_discount_per_so_line",
    )

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.env.user.group_ids |= cls.env.ref("sale.group_discount_per_so_line")
        cls.partner = cls.env["res.partner"].create(
            {"name": "Test Partner", "sale_discount": 10}
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Test Product", "type": "service", "list_price": 100}
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test multi-currency",
                "currency_id": cls.env.ref("base.USD").id,
                "item_ids": [
                    Command.create(
                        {
                            "applied_on": "1_product",
                            "compute_price": "discount",
                            "product_tmpl_id": cls.product.product_tmpl_id.id,
                            "price_discount": 20,
                        }
                    ),
                ],
            }
        )
        cls.pricelist_item = cls.pricelist.item_ids
        cls._set_discount_positions("discount2", "discount1")

    @classmethod
    def _set_discount_positions(
        cls, general_discount: str, pricelist_discount: str
    ) -> None:
        params = cls.env["ir.config_parameter"].sudo()
        params.set_str(
            "sale_order_general_discount_triple.general_discount", general_discount
        )
        params.set_str(
            "sale_order_general_discount_triple.pricelist_discount", pricelist_discount
        )

    def _create_order(self) -> models.Model:
        return self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "pricelist_id": self.pricelist.id,
                "order_line": [
                    Command.create(
                        {"product_id": self.product.id, "product_uom_qty": 2}
                    )
                ],
            }
        )
