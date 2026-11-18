# Copyright 2011 Akretion Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright 2013 Camptocamp SA (author: Guewen Baconnier)
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    workflow_process_id = fields.Many2one(
        comodel_name="sale.workflow.process", string="Sale Workflow Process"
    )

    def validate_picking(self):
        """Set quantities automatically and validate the pickings."""
        for picking in self:
            picking.action_assign()
            for move in picking.move_ids.filtered(
                lambda m: m.state not in ["done", "cancel"]
            ):
                # In Odoo 19 the reserved quantity is stored on the move lines
                # as their `quantity`; flagging the move as picked turns that
                # reserved quantity into the done quantity.
                if move.quantity:
                    move.picked = True
            picking.with_context(skip_immediate=True, skip_sms=True).button_validate()
        return True
