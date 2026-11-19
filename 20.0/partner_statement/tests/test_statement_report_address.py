# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import html

from odoo.tests.common import TransactionCase


class TestStatementReportAddress(TransactionCase):
    """The address block must reach the report layout.

    The document templates set ``address`` with ``t-set`` and hand it to
    ``web.external_layout``.  In Odoo 20 a value set inside the body of a
    ``t-call`` is no longer passed to the called template, so the address
    block silently disappears from the report.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.company.external_report_layout_id = cls.env.ref(
            "web.external_layout_standard"
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Statement Address Partner",
                "street": "12 Rue de la Paix",
                "city": "Paris",
            }
        )

    def _assert_address_block(self, report_ref):
        report = self.env["ir.actions.report"]
        report_html, _report_type = report._render_qweb_html(
            report_ref, self.partner.ids
        )
        tree = html.fromstring(report_html)
        address_blocks = tree.xpath("//div[@name='address']")
        self.assertTrue(
            address_blocks,
            "The address block is missing from the report %s." % report_ref,
        )
        address_text = " ".join(address_blocks[0].itertext())
        self.assertIn(
            self.partner.name,
            address_text,
            "The partner name is missing from the address block of %s." % report_ref,
        )

    def test_activity_statement_address_block(self):
        self._assert_address_block(
            "partner_statement.action_print_activity_statement_html"
        )

    def test_detailed_activity_statement_address_block(self):
        self._assert_address_block(
            "partner_statement.action_print_detailed_activity_statement_html"
        )

    def test_outstanding_statement_address_block(self):
        self._assert_address_block(
            "partner_statement.action_print_outstanding_statement_html"
        )
