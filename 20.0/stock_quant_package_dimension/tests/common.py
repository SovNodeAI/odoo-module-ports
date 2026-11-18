# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests import TransactionCase


class TestStockQuantPackageCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.wh = cls.env.ref("stock.warehouse0")
        cls.wh.out_type_id.default_location_dest_id = cls.env.ref(
            "stock.stock_location_customers"
        )
        # Demo data is not installed on the test bench, create the product
        cls.product = cls.env["product.product"].create(
            {"name": "Test Product", "is_storable": True, "weight": 1}
        )
        # In Odoo 20 a product packaging is a UoM available on the product
        cls.product.uom_ids = cls.env["uom.uom"].create(
            [
                {
                    "name": "Small Box",
                    "relative_factor": 1,
                    "relative_uom_id": cls.env.ref("uom.product_uom_unit").id,
                    "weight": 2,
                },
                {
                    "name": "Box",
                    "relative_factor": 5,
                    "relative_uom_id": cls.env.ref("uom.product_uom_unit").id,
                    "weight": 7,
                },
            ]
        )
        cls.package = cls.env["stock.package"].create({})
        cls.move = cls.env["stock.move"].create(
            {
                "picking_type_id": cls.wh.out_type_id.id,
                "product_id": cls.product.id,
                "product_uom_qty": 11.0,
                "uom_id": cls.product.uom_id.id,
                "location_id": cls.wh.out_type_id.default_location_src_id.id,
                "location_dest_id": cls.wh.out_type_id.default_location_dest_id.id,
                "procure_method": "make_to_stock",
            }
        )
        cls.move._assign_picking()
        cls.move.picking_id.action_confirm()
