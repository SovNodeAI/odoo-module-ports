# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSaleReportColumns(TransactionCase):
    def test_report_selects_module_field(self):
        """Odoo 20 builds the sales analysis from _select_dict() and _groupby_list().
        A field that is not in the dict is silently filled with NULL."""
        report = self.env["sale.report"]
        table = self.env["sale.order.line"]._search([]).table
        self.assertIn("lot_id", report._select_dict(table))
        self.assertIn(table.lot_id, report._groupby_list(table))
        report.search_read([], ["lot_id"], limit=1)
        report._read_group([], ["lot_id"], ["__count"])
