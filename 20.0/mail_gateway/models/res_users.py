# Copyright 2024 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.mail.tools.discuss import Store


class ResUsers(models.Model):
    _inherit = "res.users"

    gateway_ids = fields.Many2many("mail.gateway", groups="mail_gateway.gateway_user")

    def _store_init_global_fields(self, res: Store.FieldList):
        super()._store_init_global_fields(res)
        res.attr("gateways", self.sudo().gateway_ids.gateway_info())
