# Copyright 2024 ACSONE SA/NV
# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _get_returned_restricted_quantity_by_lot(
        self, stock_move, lot, exclude_move=None
    ):
        """Get the restricted quantity still available for the given lot."""
        exclude_move = exclude_move or self
        returned_qty = 0.0
        for dest_move in (stock_move.move_dest_ids - exclude_move).filtered(
            lambda sm: sm.origin_returned_move_id == stock_move
        ):
            if dest_move.move_line_ids:
                returned_qty += sum(
                    dest_move.move_line_ids.filtered(
                        lambda sml: sml.lot_id == lot
                    ).mapped("quantity")
                )
            elif dest_move.restrict_lot_id == lot and dest_move.state != "draft":
                # A pending return has no move line anymore once the core
                # unreserved it: its demand is the quantity to be returned.
                returned_qty += dest_move.product_uom_qty
        return (
            sum(
                stock_move.move_line_ids.filtered(
                    lambda sml: sml.lot_id == lot
                ).mapped("quantity")
            )
            - returned_qty
        )

    @api.model
    def get_returned_restricted_quantity(self, stock_move, exclude_move=None):
        """Get the restricted quantity still available for this move's lot."""
        exclude_move = exclude_move or self
        return self._get_returned_restricted_quantity_by_lot(
            stock_move, self.restrict_lot_id, exclude_move=exclude_move
        )

    def _check_return_quantity_by_lot(self, lot=None, quantity=None):
        for move in self:
            returned_move = move.origin_returned_move_id
            if not returned_move:
                continue
            if lot is None:
                lot = move.restrict_lot_id
            if lot:
                qty = move._get_returned_restricted_quantity_by_lot(
                    returned_move, lot, exclude_move=move
                )
            else:
                qty = move.picking_id.get_returned_restricted_quantity(
                    returned_move, exclude_move=move
                )
            if quantity is None:
                quantity = move.product_uom_qty
            if (
                returned_move.picking_id.picking_type_id.restrict_return_qty
                and quantity > qty
            ):
                raise UserError(
                    self.env._("Return more quantities than delivered is not allowed.")
                )

    @api.constrains("product_uom_qty", "restrict_lot_id")
    def _check_return_quantity_by_lot_constraint(self):
        self._check_return_quantity_by_lot()

    def write(self, vals):
        # The lot and the quantity are checked together, so that selecting a lot
        # that was not delivered reports the same error as an excessive quantity.
        if "restrict_lot_id" in vals:
            lot = self.env["stock.lot"].browse(vals["restrict_lot_id"])
            quantity = vals.get("product_uom_qty")
            self._check_return_quantity_by_lot(lot=lot, quantity=quantity)
        return super().write(vals)
