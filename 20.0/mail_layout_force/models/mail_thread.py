# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _get_substituted_layout_xmlid(self, layout_xmlid, model_name):
        layout = self.env.ref(layout_xmlid, raise_if_not_found=False)
        if not layout:
            return False
        res_model = (
            self.env["ir.model"].sudo().search([("model", "=", model_name)], limit=1)
        )
        mapping = self.env["email.layout.mapping"].search(
            [("layout_id", "=", layout.id), ("model_ids", "in", res_model.ids)],
            limit=1,
        )
        if not mapping:
            mapping = self.env["email.layout.mapping"].search(
                [("layout_id", "=", layout.id), ("model_ids", "=", False)], limit=1
            )
        if not mapping:
            return False
        substitute_layout = mapping.substitute_layout_id
        if not substitute_layout.xml_id:
            substitute_layout._export_rows([["id"]])
            # Refresh cache to get xml_id assigned by _export_rows
            substitute_layout.invalidate_recordset()
        return substitute_layout.xml_id

    def _notify_by_email_render_layout(
        self, message, recipients_group, render_values=None
    ):
        # OVERRIDE to force the layout substitution defined on the
        # email.layout.mapping model. In Odoo 20 the notification layout is
        # resolved here from the message, instead of being passed through
        # msg_vals to _notify_thread_by_email.
        layout_xmlid = message.email_layout_xmlid or "mail.mail_notification_layout"
        substitute_xmlid = self._get_substituted_layout_xmlid(
            layout_xmlid, message.model or self._name
        )
        if substitute_xmlid:
            if message.id:
                # Avoid writing on the actual message: use an in-memory copy
                message = message.new(
                    {"email_layout_xmlid": substitute_xmlid}, origin=message
                )
            else:
                # Already an in-memory message (composer, preview): just
                # override the layout in its cache
                message.email_layout_xmlid = substitute_xmlid
        return super()._notify_by_email_render_layout(
            message, recipients_group, render_values=render_values
        )
