# Copyright 2024 ACSONE SA/NV (https://www.acsone.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockPutInPack(models.TransientModel):
    _inherit = "stock.put.in.pack"

    package_type_domain = fields.Json(
        compute="_compute_package_type_domain", readonly=True
    )

    @api.depends("move_line_ids.carrier_id", "move_line_ids.picking_type_id")
    def _compute_package_type_domain(self):
        pickings = self.env["stock.picking"].browse(
            self.env.context.get("picking_ids", [])
        )
        pickings |= self.move_line_ids.picking_id
        for wizard in self:
            if not all(pickings.mapped("picking_type_id.filter_package_type_on_put_in_pack")):
                wizard.package_type_domain = []
                continue
            wizard.package_type_domain = [
                ("package_carrier_type", "=", wizard.package_carrier_type)
            ]
