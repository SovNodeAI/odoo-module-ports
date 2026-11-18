# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    rma_reason_id = fields.Many2one(
        comodel_name="rma.reason", readonly=False, string="RMA Reason"
    )
    rma_operation_domain = fields.Json(compute="_compute_rma_operation_domain")

    @api.depends("rma_reason_id")
    def _compute_rma_operation_domain(self):
        for rec in self:
            if rec.rma_reason_id and rec.rma_reason_id.allowed_operation_ids:
                rec.rma_operation_domain = [
                    ("id", "in", rec.rma_reason_id.allowed_operation_ids.ids)
                ]
            else:
                rec.rma_operation_domain = []

    def _create_return(self):
        """Propagate the reason given in the RMA wizard to the return picking."""
        new_picking = super()._create_return()
        reason_id = self.env.context.get("rma_reason_id")
        if reason_id:
            new_picking.rma_reason_id = reason_id
        return new_picking
