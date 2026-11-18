# Copyright 2020 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.constrains("product_uom_qty")
    def _check_return_quantity(self):
        for move in self:
            returned_move = move.origin_returned_move_id
            if not returned_move:
                continue
            restrict_return_qty = returned_move.picking_id.picking_type_id.restrict_return_qty
            qty = self.env["stock.picking"].get_returned_restricted_quantity(returned_move, exclude_move=self)
            if restrict_return_qty and move.product_uom_qty > qty:
                raise UserError(
                    self.env._("Return more quantities than delivered is not allowed.")
                )
