# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestCopySeveral(TransactionCase):
    """Duplicate with two rows selected in the list view: since 18.0 the web
    client copies every selected record in one call."""

    def test_duplicate_two_reports_from_the_list(self):
        reports = self.env["mis.report"].create(
            [{"name": "Report A"}, {"name": "Report B"}]
        )
        copies = reports.copy()
        self.assertEqual(
            sorted(copies.mapped("name")), ["Report A (copy)", "Report B (copy)"]
        )

    def test_duplicate_two_instances_from_the_list(self):
        report = self.env["mis.report"].create({"name": "Report"})
        instances = self.env["mis.report.instance"].create(
            [
                {"name": "Instance A", "report_id": report.id},
                {"name": "Instance B", "report_id": report.id},
            ]
        )
        copies = instances.copy()
        self.assertEqual(
            sorted(copies.mapped("name")), ["Instance A (copy)", "Instance B (copy)"]
        )
