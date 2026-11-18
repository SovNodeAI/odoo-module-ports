# Copyright 2024 Dixmit
# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged, users

from .common import MailGatewayTestCase


@tagged("post_install", "-at_install")
class TestGatewayMessagingMenu(MailGatewayTestCase, HttpCase):
    @users("admin")
    def test_gateway_tab_uses_messaging_menu_flow(self):
        self.authenticate(self.env.user.login, self.env.user.login)
        channel = self.env["discuss.channel"].create(
            {"name": "Pinned gateway", "channel_type": "gateway"}
        )
        channel._add_members(users=self.env.user)
        channel.message_post(body="Unread gateway message", message_type="comment")
        channel.self_member_id.new_message_separator = 0
        pending_channel = self.env["discuss.channel"].create(
            {"name": "Needaction gateway", "channel_type": "gateway"}
        )
        self.env["mail.message"].sudo().create(
            {
                "model": "discuss.channel",
                "res_id": pending_channel.id,
                "body": "Pending gateway message",
                "message_type": "comment",
                "notification_ids": [
                    (
                        0,
                        0,
                        {
                            "res_partner_id": self.env.user.partner_id.id,
                            "notification_type": "inbox",
                        },
                    )
                ],
            }
        )
        data = self.make_jsonrpc_request(
            "/mail/store",
            {
                "fetch_params": [
                    [
                        "/mail/messaging_menu/discuss.channel/load_more",
                        {"tab_id": "gateway", "limit": 30},
                    ],
                    [
                        "/mail/messaging_menu/initialize_counters",
                        {
                            "filter_id_by_tab_id_by_record_type": {
                                "discuss.channel": {"gateway": None},
                            }
                        },
                    ],
                ]
            },
        )
        loaded_ids = {item["id"] for item in data["discuss.channel"]}
        self.assertIn(channel.id, loaded_ids)
        self.assertTrue(pending_channel.id in loaded_ids)
        counter_ids = {
            tab["id"]: tab["init_counter_ids"] for tab in data["MessagingMenuTab"]
        }
        self.assertIn(channel.id, counter_ids["gateway"])
        self.assertIn(pending_channel.id, counter_ids["gateway"])
