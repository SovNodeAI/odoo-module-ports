# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestInvoiceReportColumns(TransactionCase):
    def test_report_reads_module_fields(self):
        """Odoo 20 builds the invoice analysis from _select_list(). A field of this
        module that is missing there makes the report fail as soon as it is read."""
        report = self.env["account.invoice.report"]
        report.search_read([], ["product_brand_id"], limit=1)
        for groupby in ["product_brand_id"]:
            report._read_group([], [groupby], ["__count"])
