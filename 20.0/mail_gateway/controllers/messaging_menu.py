# Copyright 2024 Dixmit
# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.fields import Domain
from odoo.addons.mail.controllers.webclient import WebclientController


class GatewayMessagingMenuController(WebclientController):
    def _get_menu_tab_domain(self, tab_id):
        if tab_id != "gateway":
            return super()._get_menu_tab_domain(tab_id)
        channel_ids = self._get_pinned_gateway_channel_ids()
        if self.env.user._is_internal():
            channel_ids += self._get_needaction_gateway_channel_ids()
        return Domain("channel_type", "=", "gateway") & Domain("id", "in", channel_ids)

    def store_messaging_menu_initialize_counters(
        self, store, filter_id_by_tab_id_by_record_type
    ):
        super().store_messaging_menu_initialize_counters(
            store,
            filter_id_by_tab_id_by_record_type=filter_id_by_tab_id_by_record_type,
        )
        filter_id_by_tab_id = filter_id_by_tab_id_by_record_type.get("discuss.channel")
        if not filter_id_by_tab_id or "gateway" not in filter_id_by_tab_id:
            return
        domain_by_tab_id = self.get_menu_counter_domain_by_tab_id(
            {"gateway": filter_id_by_tab_id["gateway"]}
        )
        unread_channel_ids = self.env["discuss.channel.member"].sudo().search_fetch(
            [
                ("is_self", "=", True),
                ("is_pinned", "=", True),
                ("is_unread", "=", True),
                ("mute_until_dt", "=", False),
                ("channel_id.channel_type", "=", "gateway"),
            ]
        ).channel_id.ids
        important_domain = Domain("id", "in", unread_channel_ids)
        if self.env.user._is_internal():
            important_domain |= Domain(
                "id", "in", self._get_needaction_gateway_channel_ids()
            )
        candidate_channels = self.env["discuss.channel"].search_fetch(
            Domain("channel_type", "=", "gateway") & important_domain
        )
        self._add_menu_tab_counters_to_store(
            store, candidate_channels, domain_by_tab_id
        )

    def _get_needaction_gateway_channel_ids(self):
        groups = self.env["mail.message"]._read_group(
            [
                ("model", "=", "discuss.channel"),
                ("message_type", "!=", "user_notification"),
                ("needaction", "=", True),
            ],
            ["res_id"],
        )
        return list(
            set(res_id for [res_id] in groups)
            & set(
                self.env["discuss.channel"].search_fetch(
                    Domain("channel_type", "=", "gateway")
                ).ids
            )
        )

    def _get_pinned_gateway_channel_ids(self):
        return self.env["discuss.channel.member"].sudo().search_fetch(
            [
                ("is_self", "=", True),
                ("is_pinned", "=", True),
                ("channel_id.channel_type", "=", "gateway"),
            ]
        ).channel_id.ids
