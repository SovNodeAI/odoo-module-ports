# Copyright 2024 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.mail.tools.discuss import Store


class MailGuest(models.Model):
    _inherit = "mail.guest"

    gateway_id = fields.Many2one("mail.gateway")
    gateway_token = fields.Char()

    def _store_avatar_fields(self, res: Store.FieldList):
        super()._store_avatar_fields(res)
        res.attr("gateway_id")
