# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from lxml import html

from odoo import fields
from odoo.tests.common import TransactionCase


class TestAccountBillingReport(TransactionCase):
    def test_report_billing_receives_address(self):
        partner = self.env["res.partner"].create(
            {"name": "Billing Report Address Partner"}
        )
        billing = self.env["account.billing"].create(
            {"partner_id": partner.id, "threshold_date": fields.Date.today()}
        )

        report = self.env["ir.actions.report"]._render_qweb_html(
            "account_billing.report_billing", billing.ids
        )[0]
        addresses = html.fromstring(report).xpath(
            "//div[@name='address']//address"
        )

        self.assertTrue(addresses)
        self.assertIn(partner.name, addresses[0].text_content())
