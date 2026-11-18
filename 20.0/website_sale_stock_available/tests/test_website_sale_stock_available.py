# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.website_sale.tests.common import MockRequest


class SaleStockAvailableInfoPopup(BaseCommon):
    _test_user_groups = ("base.group_user", "stock.group_stock_user")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user_group_stock_user = cls.env.ref("stock.group_stock_user")
        cls.user_stock_user = cls.env["res.users"].create(
            {
                "name": "Pauline Poivraisselle",
                "login": "pauline",
                "email": "p.p@example.com",
                "notification_type": "inbox",
                "group_ids": [Command.link(user_group_stock_user.id)],
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Storable product",
                "type": "consu",
                "is_storable": True,
            }
        )
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customers_location = cls.env.ref("stock.stock_location_customers")
        cls.suppliers_location = cls.env.ref("stock.stock_location_suppliers")
        cls.group_user._apply_group(cls.env.ref("product.group_product_pricelist"))
        cls.pricelist = cls.env["product.pricelist"].create({
            "name": "Test Pricelist",
            "website_id": cls.env.ref("base.default_website").id,
        })
        cls.env["stock.quant"].create(
            {
                "product_id": cls.product.id,
                "location_id": cls.stock_location.id,
                "quantity": 40.0,
            }
        )
        cls.picking_out = cls.env["stock.picking"].create(
            {
                "picking_type_id": cls.env.ref("stock.picking_type_out").id,
                "location_id": cls.stock_location.id,
                "location_dest_id": cls.customers_location.id,
            }
        )
        cls.env["stock.move"].create(
            {
                "product_id": cls.product.id,
                "product_uom_qty": 3.0,
                "uom_id": cls.product.uom_id.id,
                "picking_id": cls.picking_out.id,
                "location_id": cls.stock_location.id,
                "location_dest_id": cls.customers_location.id,
            }
        )
        cls.picking_in = cls.env["stock.picking"].create(
            {
                "picking_type_id": cls.env.ref("stock.picking_type_in").id,
                "location_id": cls.suppliers_location.id,
                "location_dest_id": cls.stock_location.id,
            }
        )
        cls.env["stock.move"].create(
            {
                "restrict_partner_id": cls.user_stock_user.partner_id.id,
                "product_id": cls.product.id,
                "product_uom_qty": 5.0,
                "uom_id": cls.product.uom_id.id,
                "picking_id": cls.picking_in.id,
                "location_id": cls.suppliers_location.id,
                "location_dest_id": cls.stock_location.id,
            }
        )

    def test_get_combination_info(self):
        product_tmpl = self.product.product_tmpl_id
        website = self.env["website"].search([], limit=1)
        with MockRequest(
            self.env, website=website, website_sale_current_pl=self.pricelist.id
        ) as request:
            request.update_context(website_sale_product_page=True)
            product_tmpl = product_tmpl.with_env(request.env)
            combination_info = product_tmpl.with_context(
                website_sale_stock_get_quantity=True,
            )._get_combination_info(pricelist=self.pricelist)
            self.assertEqual(
                combination_info["free_qty"],
                40,
            )
            self.picking_out.action_confirm()
            self.picking_in.action_assign()
            combination_info = product_tmpl.with_context(
                website_sale_stock_get_quantity=True,
            )._get_combination_info(pricelist=self.pricelist)
            self.assertEqual(
                combination_info["free_qty"], self.product.immediately_usable_qty
            )
