# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import html

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestOverdueReminderReport(TransactionCase):
    def test_report_renders_partner_address(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Overdue Report Recipient 2026",
                "street": "42 Reminder Street",
            }
        )
        step = self.env["overdue.reminder.step"].create(
            {
                "partner_id": partner.id,
                "commercial_partner_id": partner.id,
                "user_id": self.env.user.id,
            }
        )

        report_html, _report_format = self.env["ir.actions.report"]._render_qweb_html(
            "account_invoice_overdue_reminder.overdue_reminder_step_report", step.ids
        )
        address_blocks = html.fromstring(report_html).xpath("//div[@name='address']")
        self.assertEqual(len(address_blocks), 1)
        self.assertIn(partner.name, address_blocks[0].text_content())
