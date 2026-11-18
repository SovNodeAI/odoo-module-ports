# Copyright 2020 Iryna Vyshnevska Camptocamp
# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from collections import defaultdict

from odoo import Command, api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _get_qty_by_lot(self, move):
        """Get all quantities that were shipped out, per lot"""
        qties = defaultdict(float)
        move.invalidate_recordset(["move_dest_ids"])
        for sml in move.move_line_ids:
            qties[sml.lot_id] += sml.quantity
        for dest_move in move.move_dest_ids:
            if dest_move.origin_returned_move_id == move:
                if dest_move.move_line_ids:
                    for sml in dest_move.move_line_ids:
                        qties[sml.lot_id] -= sml.quantity
                else:
                    # A pending return has no move line anymore once the core
                    # unreserved it when a new return was created: its demand
                    # is the quantity that is going to be returned.
                    qties[dest_move.restrict_lot_id] -= dest_move.product_uom_qty
        return qties

    def _split_return_moves_by_lot(self, qties_by_move=None):
        """Create an editable return move for each lot shipped by each move."""
        for picking in self.filtered("return_id"):
            moves_to_unlink = self.env["stock.move"]
            new_move_values = []
            for move in picking.move_ids:
                origin_move = move.origin_returned_move_id
                if not origin_move:
                    continue
                if qties_by_move is not None and origin_move in qties_by_move:
                    qties = qties_by_move[origin_move]
                else:
                    qties = self._get_qty_by_lot(origin_move)
                lot_qties = [(lot, qty) for lot, qty in qties.items() if qty > 0]
                if not lot_qties:
                    continue
                move_values = move.copy_data()[0]
                move_values.pop("move_line_ids", None)
                move_values.pop("lot_ids", None)
                move_values["move_orig_ids"] = [Command.set(move.move_orig_ids.ids)]
                moves_to_unlink |= move
                for lot, qty in lot_qties:
                    new_move_values.append(
                        dict(
                            move_values,
                            picking_id=picking.id,
                            restrict_lot_id=lot.id,
                            origin_returned_move_id=origin_move.id,
                            product_uom_qty=qty if not picking.show_return else 0,
                        )
                    )
            moves_to_unlink.unlink()
            if new_move_values:
                self.env["stock.move"].create(new_move_values)

    def get_returned_restricted_quantity(self, stock_move, exclude_move=None):
        """Restrict the quantity by the return move's lot, if one is selected."""
        if self.return_id and exclude_move and exclude_move.restrict_lot_id:
            return exclude_move.get_returned_restricted_quantity(
                stock_move, exclude_move=exclude_move
            )
        return super().get_returned_restricted_quantity(
            stock_move, exclude_move=exclude_move
        )

    def _create_return(self):
        # Odoo 20 creates an editable return picking instead of a return wizard.
        # The core unreserves the previous returns before copying the moves, so
        # the quantities already returned per lot must be computed beforehand.
        qties_by_move = {
            move: self._get_qty_by_lot(move)
            for move in self.move_ids.filtered(lambda m: m.state != "cancel")
        }
        picking = super()._create_return()
        picking._split_return_moves_by_lot(qties_by_move)
        return picking

    def _reset_quantities(self):
        """When asked to return all quantities, reset to restricted quantity per lot"""
        for move in self.move_ids:
            if move.origin_returned_move_id:
                move.product_uom_qty = self.get_returned_restricted_quantity(
                    move.origin_returned_move_id, exclude_move=move
                )

    def action_return_all(self):
        """Force a reset to returnable quantities per lot"""
        result = super().action_return_all()
        self._reset_quantities()
        return result
