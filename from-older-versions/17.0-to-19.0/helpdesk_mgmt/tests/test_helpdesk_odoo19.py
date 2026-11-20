# Copyright 2026 SovNode AI
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from lxml import etree

from .common import TestHelpdeskTicketBase


class TestHelpdeskOdoo19(TestHelpdeskTicketBase):
    def test_stage_group_expand(self):
        unused_stage = self.env["helpdesk.ticket.stage"].create(
            {"name": "Unused Team A stage", "team_ids": [(6, 0, self.team_a.ids)]}
        )
        other_team_stage = self.env["helpdesk.ticket.stage"].create(
            {"name": "Team B only stage", "team_ids": [(6, 0, self.team_b.ids)]}
        )
        tickets = self.ticket_a_unassigned | self.ticket_a_user_own
        result = (
            self.env["helpdesk.ticket"]
            .with_context(default_team_id=self.team_a.id, read_group_expand=True)
            .web_read_group(
                domain=[("id", "in", tickets.ids)],
                groupby=["stage_id"],
                aggregates=["__count"],
            )
        )
        stage_ids = {
            group["stage_id"][0] for group in result["groups"] if group["stage_id"]
        }
        self.assertIn(unused_stage.id, stage_ids)
        self.assertNotIn(other_team_stage.id, stage_ids)

    def test_suggested_recipients_with_customer_partner(self):
        partner = self.env["res.partner"].create(
            {"name": "Helpdesk Customer", "email": "customer@example.com"}
        )
        self.ticket_a_unassigned.partner_email = False
        self.ticket_a_unassigned.partner_id = partner
        recipients = self.ticket_a_unassigned._message_get_suggested_recipients(
            reply_discussion=True, no_create=True
        )
        self.assertIn(partner.id, [recipient["partner_id"] for recipient in recipients])

    def test_suggested_recipients_without_customer_partner(self):
        self.ticket_a_unassigned.partner_id = False
        self.ticket_a_unassigned.partner_email = "customer-email@example.com"
        recipients = self.ticket_a_unassigned._message_get_suggested_recipients(
            no_create=True
        )
        self.assertIn(
            "customer-email@example.com",
            [recipient["email"] for recipient in recipients],
        )

    def test_multi_ticket_copy_gets_unique_numbers(self):
        tickets = self.ticket_a_unassigned | self.ticket_a_user_own
        copies = tickets.copy()
        self.assertEqual(len(copies), 2)
        self.assertEqual(copies.mapped("name"), tickets.mapped("name"))
        self.assertNotIn("/", copies.mapped("number"))
        self.assertEqual(len(set(copies.mapped("number"))), 2)
        self.assertFalse(set(copies.mapped("number")) & set(tickets.mapped("number")))

    def test_kanban_views_use_odoo19_templates(self):
        views = [
            ("helpdesk_mgmt.helpdesk_ticket_kanban_view", "kanban"),
            ("helpdesk_mgmt.view_helpdesk_ticket_kanban", "kanban"),
            ("helpdesk_mgmt.view_helpdesk_team_form", "form"),
        ]
        arches = {}
        for xmlid, view_type in views:
            with self.subTest(view=xmlid):
                view = self.env.ref(xmlid)
                # each view is read through its own model (the dashboard kanban
                # belongs to the team model), as the web client reads it
                arch = etree.fromstring(
                    self.env[view.model].get_view(view.id, view_type)["arch"]
                )
                arches[xmlid] = arch
                self.assertTrue(arch.xpath(".//t[@t-name='card']"))
                self.assertFalse(arch.xpath(".//t[@t-name='kanban-box']"))
                self.assertFalse(arch.xpath(".//t[@t-name='kanban-menu']"))

        dashboard_arch = arches["helpdesk_mgmt.helpdesk_ticket_kanban_view"]
        self.assertTrue(
            dashboard_arch.xpath(".//field[@widget='kanban_color_picker']")
        )
        ticket_arch = arches["helpdesk_mgmt.view_helpdesk_ticket_kanban"]
        self.assertTrue(ticket_arch.xpath(".//field[@widget='kanban_color_picker']"))
        self.assertTrue(ticket_arch.xpath(".//a[@type='open']"))
        self.assertEqual(ticket_arch.get("highlight_color"), "color")
        team_arch = arches["helpdesk_mgmt.view_helpdesk_team_form"]
        self.assertTrue(
            team_arch.xpath(".//kanban//field[@name='image_128' and @widget='image']")
        )

    def test_form_views_use_chatter_component(self):
        for model, xmlid in [
            ("helpdesk.ticket", "helpdesk_mgmt.ticket_view_form"),
            ("helpdesk.ticket.team", "helpdesk_mgmt.view_helpdesk_team_form"),
        ]:
            with self.subTest(view=xmlid):
                view_id = self.env.ref(xmlid).id
                arch = etree.fromstring(
                    self.env[model].get_view(view_id, "form")["arch"]
                )
                self.assertEqual(len(arch.xpath(".//chatter")), 1)
                self.assertFalse(
                    arch.xpath(
                        ".//*[contains(concat(' ', normalize-space(@class), ' '), "
                        "' oe_chatter ')]"
                    )
                )
                self.assertFalse(
                    arch.xpath(
                        ".//field[@widget='mail_followers' or "
                        "@widget='mail_activity' or @widget='mail_thread']"
                    )
                )
