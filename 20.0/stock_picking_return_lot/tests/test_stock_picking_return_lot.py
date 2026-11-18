# Copyright 2020 Iryna Vyshnevska Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import Form
from odoo.tools import mute_logger

from odoo.addons.base.tests.common import BaseCommon


class StockPickingReturnLotTest(BaseCommon):
    # Odoo 20's BaseCommon runs the tests as a dedicated test user; it needs
    # the stock groups the module's flows require.
    _test_user_groups = (
        "base.group_user",
        "stock.group_stock_user",
        "stock.group_stock_manager",
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.picking_obj = cls.env["stock.picking"]
        cls.partner = cls.env["res.partner"].create({"name": "Test"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "test_product",
                "type": "consu",
                "is_storable": True,
                "tracking": "lot",
            }
        )
        cls.lot_1 = cls.env["stock.lot"].create(
            {"name": "000001", "product_id": cls.product.id}
        )
        cls.lot_2 = cls.env["stock.lot"].create(
            {"name": "000002", "product_id": cls.product.id}
        )
        cls.lot_3 = cls.env["stock.lot"].create(
            {"name": "000003", "product_id": cls.product.id}
        )
        warehouse = cls.env["stock.warehouse"].search(
            [
                ("company_id", "=", cls.env.company.id),
            ]
        )
        cls.picking_type_out = warehouse.out_type_id
        cls.stock_location = warehouse.lot_stock_id
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.env["stock.quant"]._update_available_quantity(
            cls.product, cls.stock_location, 1, lot_id=cls.lot_1
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.product, cls.stock_location, 2, lot_id=cls.lot_2
        )
        cls.picking = cls.picking_obj.create(
            {
                "partner_id": cls.partner.id,
                "picking_type_id": cls.picking_type_out.id,
                "location_id": cls.stock_location.id,
                "location_dest_id": cls.customer_location.id,
                "move_ids": [
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "product_uom_qty": 3,
                            "uom_id": cls.product.uom_id.id,
                            "location_id": cls.stock_location.id,
                            "location_dest_id": cls.customer_location.id,
                        },
                    )
                ],
            }
        )
        cls.picking.action_confirm()
        cls.picking.move_ids.picked = True
        cls.picking._action_done()

    @classmethod
    def create_return_wiz(cls, picking):
        return picking._create_return()

    def _create_picking(self, product=None):
        if not product:
            product = self.product
        picking = self.picking_obj.create(
            {
                "partner_id": self.partner.id,
                "picking_type_id": self.picking_type_out.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "move_ids": [
                    Command.create(
                        {
                            "product_id": product.id,
                            "product_uom_qty": 1,
                            "uom_id": product.uom_id.id,
                            "location_id": self.stock_location.id,
                            "location_dest_id": self.customer_location.id,
                        },
                    ),
                ],
            }
        )
        self.env["stock.move"].create(
            {
                "picking_id": picking.id,
                "product_id": product.id,
                "description_picking": "extra-move",
                "product_uom_qty": 1,
                "uom_id": self.product.uom_id.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        return picking

    def _create_validate_picking(self):
        picking = self._create_picking()
        picking.action_confirm()
        picking.move_ids.picked = True
        picking._action_done()
        return picking

    def test_restrict_qty(self):
        self.picking.picking_type_id.restrict_return_qty = True
        return_picking = self.create_return_wiz(self.picking)
        return_line = return_picking.move_ids.filtered(
            lambda m, lot=self.lot_1: m.restrict_lot_id == lot
        )
        with self.assertRaisesRegex(
            UserError, "more quantities than delivered is not allowed"
        ):
            return_line.product_uom_qty = 2
        self.picking.picking_type_id.restrict_return_qty = False
        return_line.product_uom_qty = 2
        self.assertEqual(return_line.product_uom_qty, 2)
        return_picking.action_return()

    def test_incorrect_lot(self):
        self.picking.picking_type_id.restrict_return_qty = True
        return_picking = self.create_return_wiz(self.picking)
        return_line = return_picking.move_ids.filtered(
            lambda m, lot=self.lot_1: m.restrict_lot_id == lot
        )
        with self.assertRaisesRegex(
            UserError, "more quantities than delivered is not allowed"
        ):
            return_line.restrict_lot_id = self.lot_3
        self.picking.picking_type_id.restrict_return_qty = False
        return_picking.action_return()

    def test_partial_return(self):
        return_picking = self.create_return_wiz(self.picking)
        self.assertEqual(len(return_picking.move_ids), 2)
        return_line_1 = return_picking.move_ids.filtered(
            lambda m, lot=self.lot_1: m.restrict_lot_id == lot
        )
        return_line_2 = return_picking.move_ids.filtered(
            lambda m, lot=self.lot_2: m.restrict_lot_id == lot
        )
        self.assertEqual(return_line_1.product_uom_qty, 1)
        self.assertEqual(return_line_2.product_uom_qty, 2)
        return_line_2.product_uom_qty = 1
        picking_returned = self.picking_obj.browse(return_picking.id)
        picking_returned.action_confirm()
        picking_returned.action_assign()
        move_1 = picking_returned.move_ids.filtered(
            lambda m, lot=self.lot_1: m.restrict_lot_id == lot
        )
        move_2 = picking_returned.move_ids.filtered(
            lambda m, lot=self.lot_2: m.restrict_lot_id == lot
        )
        self.assertEqual(move_1.move_line_ids.lot_id, self.lot_1)
        self.assertEqual(move_2.move_line_ids.lot_id, self.lot_2)
        self.assertEqual(move_2.product_qty, 1)

    @mute_logger("odoo.models.unlink")
    def test_full_return_after_partial_return(self):
        self.test_partial_return()
        return_picking = self.create_return_wiz(self.picking)
        # Lot 1 has been fully returned already, so it isn't suggested anymore
        self.assertEqual(len(return_picking.move_ids), 1)
        self.assertEqual(return_picking.move_ids.restrict_lot_id, self.lot_2)
        self.assertEqual(return_picking.move_ids.product_uom_qty, 1)
        return_picking.action_return_all()
        picking_returned = self.picking_obj.browse(return_picking.id)
        picking_returned.action_confirm()
        picking_returned.action_assign()
        move_1 = picking_returned.move_ids.filtered(
            lambda m, lot=self.lot_1: m.restrict_lot_id == lot
        )
        move_2 = picking_returned.move_ids.filtered(
            lambda m, lot=self.lot_2: m.restrict_lot_id == lot
        )
        self.assertFalse(move_1)
        self.assertEqual(move_2.move_line_ids.lot_id, self.lot_2)
        self.assertEqual(move_2.product_qty, 1)

    @mute_logger("odoo.models.unlink")
    def test_multiple_move_same_product_different_lot(self):
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.stock_location, 1, lot_id=self.lot_1
        )
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.stock_location, 1, lot_id=self.lot_2
        )
        picking = self._create_validate_picking()
        return_picking = self.create_return_wiz(picking)
        self.assertEqual(len(return_picking.move_ids), 2)
        return_line_1 = return_picking.move_ids.filtered(
            lambda m, lot=self.lot_1: m.restrict_lot_id == lot
        )
        return_line_2 = return_picking.move_ids.filtered(
            lambda m, lot=self.lot_2: m.restrict_lot_id == lot
        )
        self.assertEqual(return_line_1.product_uom_qty, 1)
        self.assertEqual(return_line_2.product_uom_qty, 1)
        return_picking.action_return_all()
        picking_returned = self.picking_obj.browse(return_picking.id)
        picking_returned.action_confirm()
        picking_returned.action_assign()
        move_1 = picking_returned.move_ids.filtered(
            lambda m, lot=self.lot_1: m.restrict_lot_id == lot
        )
        move_2 = picking_returned.move_ids.filtered(
            lambda m, lot=self.lot_2: m.restrict_lot_id == lot
        )
        self.assertEqual(move_1.move_line_ids.lot_id, self.lot_1)
        self.assertEqual(move_2.move_line_ids.lot_id, self.lot_2)
        self.assertEqual(move_2.product_qty, 1)

    @mute_logger("odoo.models.unlink")
    def test_multiple_move_same_product_same_lot(self):
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.stock_location, 2, lot_id=self.lot_1
        )
        picking = self._create_validate_picking()
        self.assertEqual(len(picking.move_ids), 2)
        return_picking = self.create_return_wiz(picking)
        self.assertEqual(len(return_picking.move_ids), 2)
        return_lines = return_picking.move_ids.filtered(
            lambda m, lot=self.lot_1: m.restrict_lot_id == lot
        )
        self.assertEqual(return_lines[0].product_uom_qty, 1)
        self.assertEqual(return_lines[1].product_uom_qty, 1)
        return_picking.action_return_all()
        picking_returned = self.picking_obj.browse(return_picking.id)
        picking_returned.action_confirm()
        picking_returned.action_assign()
        moves = picking_returned.move_ids.filtered(
            lambda m, lot=self.lot_1: m.restrict_lot_id == lot
        )
        self.assertEqual(moves.move_line_ids.lot_id, self.lot_1)
        self.assertEqual(moves[0].product_qty, 1)
        self.assertEqual(moves[1].product_qty, 1)

    def test_return_wizard_form(self):
        # Test that no AttributeError ('int' object has no attribute 'origin')
        # is raised when initializing the form
        return_picking = self.create_return_wiz(self.picking)
        return_picking_form = Form(return_picking)
        self.assertEqual(len(return_picking_form.move_ids), 2)
