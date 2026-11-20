# Copyright 2026 Engenere - Felipe Motter Pereira
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    dfe_notification = fields.Boolean(
        string="DF-e Notification",
        help=(
            "Receive Inbox notifications when the DF-e "
            "distribution finds new third-party documents."
        ),
        user_writeable=True,
    )
