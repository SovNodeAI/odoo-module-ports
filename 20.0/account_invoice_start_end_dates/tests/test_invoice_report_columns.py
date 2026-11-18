# Copyright 2026 SovNode AI
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestInvoiceReportColumns(TransactionCase):
    def test_report_reads_module_fields(self):
        """Odoo 20 builds the invoice analysis from _select_list(). A field of this
        module that is missing there makes the report fail as soon as it is read."""
        report = self.env["account.invoice.report"]
        report.search_read([], ["start_date", "end_date"], limit=1)
        for groupby in ["start_date:month", "end_date:month"]:
            report._read_group([], [groupby], ["__count"])
