# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import SUPERUSER_ID
from odoo.tests import common


class TestPurchaseRequestProcurement(common.TransactionCase):
    def setUp(self):
        super().setUp()

        # Get required Model
        self.pr_model = self.env["purchase.request"]
        self.prl_model = self.env["purchase.request.line"]
        self.product_uom_model = self.env["uom.uom"]
        self.location = self.env.ref("stock.stock_location_stock")
        self.customer_location = self.env.ref("stock.stock_location_customers")

        # Get required Model data
        self.route_buy = self.env.ref("purchase_stock.route_warehouse0_buy")
        self.product_1 = self.env["product.product"].create(
            {"name": "Chair", "is_storable": True}
        )
        self.product_1.purchase_request = True

        # Create Supplier
        self.supplier = self.env["res.partner"].create(
            {"name": "Supplier", "is_company": True, "company_id": False}
        )

        # Add supplier to product_1
        self.product_1.write(
            {
                "seller_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": self.supplier.id,
                            "price": 100.0,
                            "company_id": False,
                        },
                    )
                ]
            }
        )

    def procurement_group_run(self, name, origin, product, qty):
        """Create an outgoing move and procure it."""
        move = self.env["stock.move"].create(
            {
                "location_dest_id": self.customer_location.id,
                "location_id": self.location.id,
                "origin": origin,
                "procure_method": "make_to_order",
                "product_id": product.id,
                "product_uom": product.uom_id.id,
                "product_uom_qty": qty,
                "route_ids": [(4, self.route_buy.id)],
            }
        )
        move._action_confirm()
        return move

    def test_procure_purchase_request(self):
        move = self.procurement_group_run(
            "Test Purchase Request Procurement",
            "Test Purchase Request Procurement",
            self.product_1,
            10,
        )
        self.assertTrue(move.created_purchase_request_line_id)
        pr = move.created_purchase_request_line_id.request_id
        self.assertTrue(pr.to_approve_allowed)
        self.assertEqual(pr.origin, "Test Purchase Request Procurement")
        prl = self.env["purchase.request.line"].search([("request_id", "=", pr.id)])
        self.assertEqual(prl.request_id, pr)
        # Test split(", ")
        vals = {
            "picking_type_id": self.env.ref("stock.picking_type_in").id,
            "requested_by": SUPERUSER_ID,
            "origin": "Test Origin",
            "line_ids": [
                [
                    0,
                    0,
                    {
                        "product_id": self.product_1.id,
                        "product_uom_id": self.env.ref("uom.product_uom_unit").id,
                        "product_qty": 2.0,
                    },
                ]
            ],
        }
        self.pr_model.create(vals)
        move2 = self.procurement_group_run(
            "Test Test, Split", "Test, Split", self.product_1, 10
        )
        pr2 = move2.created_purchase_request_line_id.request_id
        self.assertEqual(pr2.origin, "Test Origin, Test, Split")
        move3 = self.procurement_group_run("Test Test, Split", False, self.product_1, 10)
        self.assertEqual(move3.created_purchase_request_line_id.request_id, pr2)
        self.assertEqual(pr2.origin, "Test Origin, Test, Split")
