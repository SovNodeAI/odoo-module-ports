# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_rma_vals(self):
        vals = super()._prepare_rma_vals()
        origin_move = self.origin_returned_move_id or self
        lot = self.restrict_lot_id
        vals["lot_id"] = lot.id
        if not origin_move.restrict_lot_id:
            smls = origin_move.move_line_ids.filtered(lambda x: x.lot_id == lot)
            vals["product_uom_qty"] = sum(smls.mapped("quantity"))
        return vals
