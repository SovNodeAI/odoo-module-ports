# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSaleReportBrand(TransactionCase):
    def test_sale_report_shows_brand(self):
        """The brand of the product has to reach the sales analysis. Odoo 20 builds
        that report from _select_dict() and fills a field it does not find with NULL."""
        brand = self.env["product.brand"].create({"name": "Report brand"})
        product = self.env["product.product"].create(
            {"name": "Branded product", "product_brand_id": brand.id}
        )
        partner = self.env["res.partner"].create({"name": "Report customer"})
        order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "order_line": [
                    Command.create({"product_id": product.id, "product_uom_qty": 1})
                ],
            }
        )
        self.env.flush_all()
        rows = self.env["sale.report"].search([("name", "=", order.name)])
        self.assertTrue(rows)
        self.assertEqual(rows.product_brand_id, brand)
        groups = self.env["sale.report"]._read_group(
            [("name", "=", order.name)], ["product_brand_id"], ["__count"]
        )
        self.assertEqual(groups, [(brand, 1)])
