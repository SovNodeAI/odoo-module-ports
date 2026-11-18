# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models
from odoo.tools import html2plaintext


class MailTrackMixin(models.AbstractModel):
    _inherit = "mail.track.mixin"

    def _create_mail_tracking_values(self, initial_value, new_value, col_name, col_info):
        try:
            return super()._create_mail_tracking_values(
                initial_value, new_value, col_name, col_info
            )
        except NotImplementedError:
            if col_info["type"] == "html":
                col_info = dict(col_info, type="text")
                values = super()._create_mail_tracking_values(
                    initial_value, new_value, col_name, col_info
                )
                values.update(
                    {
                        "old_value_char": html2plaintext(initial_value) or "",
                        "new_value_char": html2plaintext(new_value) or "",
                    }
                )
                return values
            raise
