# Copyright 2020 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _prepare_return_move_default_values(self, move_id):
        vals = super()._prepare_return_move_default_values(move_id)
        vals["product_uom_qty"] = self.get_returned_restricted_quantity(move_id)
        return vals

    def action_return_all(self):
        # Do not call super(): it would first write the original done quantity,
        # which can be above the quantity still returnable (e.g. when another
        # pending return already exists) and would trip the quantity constraint.
        self.ensure_one()
        if self.return_id:
            for return_move in self.move_ids.filtered(
                lambda m: m.state not in ("done", "cancel")
            ):
                returned_move = return_move.origin_returned_move_id
                if returned_move:
                    return_move.product_uom_qty = self.get_returned_restricted_quantity(
                        returned_move, exclude_move=return_move
                    )
        return True

    def _create_return(self):
        # Odoo 20 creates an editable return picking. Its moves are checked by
        # the stock.move constraint when a quantity is assigned or confirmed.
        return super()._create_return()

    @api.model
    def get_returned_restricted_quantity(self, stock_move, exclude_move=None):
        """Return the quantity still available to be returned for a stock move."""
        exclude_move = exclude_move or self.env["stock.move"]
        stock_move.invalidate_recordset(["move_dest_ids"])
        stock_move.returned_move_ids.invalidate_recordset(["move_orig_ids", "move_dest_ids"])
        qty = stock_move.product_qty
        moves = (
            (stock_move.move_orig_ids | stock_move.move_dest_ids) | stock_move.returned_move_ids
        )
        moves |= moves.move_dest_ids | moves.move_orig_ids
        for move in moves - exclude_move:
            if move == stock_move:
                continue
            if move.origin_returned_move_id and move.origin_returned_move_id != stock_move:
                continue
            if move.state == "cancel":
                continue
            if move.state == "draft":
                # Odoo 20 creates the return picking in draft state, without any
                # move line, so its demand is the only trace of the pending
                # return. Count it so a not yet validated return also consumes
                # the quantity available to further returns.
                if move.origin_returned_move_id == stock_move:
                    qty -= move.product_qty
                continue
            qty -= sum(move.move_line_ids.mapped("quantity"))
        return max(qty, 0.0)
