# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml.html import document_fromstring

from odoo.tests import HttpCase, tagged

from odoo.addons.http_routing.tests.common import MockRequest


@tagged("post_install", "-at_install")
class TestRecordsetFullReport(HttpCase):
    def test_full_report_body_classname(self):
        backend = self.env["import.backend"].create(
            {"name": "Report test", "version": "1.0"}
        )
        import_type = self.env["import.type"].create(
            {"name": "Report test", "key": "report_test"}
        )
        recordset = self.env["import.recordset"].create(
            {"backend_id": backend.id, "import_type_id": import_type.id}
        )
        report = self.env["ir.actions.report"].create(
            {
                "name": "Test full recordset report",
                "model": "import.recordset",
                "report_name": "connector_importer.recordset_report_full",
                "report_type": "qweb-html",
            }
        )

        with MockRequest(self.env):
            html, _ = self.env["ir.actions.report"]._render_qweb_html(
                report.id,
                recordset.ids,
                data={"recordset": recordset, "report": ""},
            )

        body = document_fromstring(html).find("body")
        self.assertIsNotNone(body)
        self.assertIn("import_recordset_report", body.get("class", "").split())
