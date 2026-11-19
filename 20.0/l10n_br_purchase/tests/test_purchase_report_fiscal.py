# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, TransactionCase, tagged

from .tools import load_purchase_fixture_files


@tagged("post_install", "-at_install")
class TestPurchaseReportFiscal(TransactionCase):
    """The fiscal columns of the purchase analysis must reach the report.

    Odoo 20 builds purchase.report from _select_list() and _groupby_list().
    A module that still extends _select()/_group_by() installs and passes its
    tests, but its columns are missing from the report: reading them raises
    "column does not exist". These tests read every field the module adds
    through the report model itself (search_read and _read_group).
    """

    REPORT_FIELDS = [
        "fiscal_operation_id",
        "fiscal_operation_line_id",
        "cfop_id",
        "fiscal_type",
        "cest_id",
        "ncm_id",
        "nbm_id",
        "icms_value",
        "icmsst_value",
        "ipi_value",
        "pis_value",
        "cofins_value",
        "ii_value",
        "freight_value",
        "insurance_value",
        "other_value",
        "total_with_taxes",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_purchase_fixture_files(cls.env)
        cls.company = cls.env.ref("l10n_br_base.empresa_lucro_presumido")
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                allowed_company_ids=cls.company.ids,
                tracking_disable=True,
            )
        )
        cls.env.user.company_ids += cls.company
        cls.env.user.company_id = cls.company
        cls.partner = cls.env.ref("l10n_br_base.res_partner_amd")
        # Physical product with NCM 7326.90.90 so ICMS and IPI are mapped.
        cls.product = cls.env.ref("product.product_product_7")
        cls.product.standard_price = 100.0

        order_form = Form(
            cls.env["purchase.order"].with_context(default_company_id=cls.company.id)
        )
        order_form.partner_id = cls.partner
        with order_form.order_line.new() as line_form:
            line_form.product_id = cls.product
            line_form.product_qty = 10.0
        cls.order = order_form.save()
        cls.env.flush_all()
        cls.line = cls.order.order_line.filtered(lambda ln: not ln.display_type)

    def _report_domain(self):
        return [("order_id", "=", self.order.id)]

    def test_report_fields_are_readable(self):
        """search_read must return every field the module adds to the report."""
        rows = self.env["purchase.report"].search_read(
            self._report_domain(), self.REPORT_FIELDS
        )
        self.assertEqual(len(rows), 1, "The purchase analysis should have one row.")
        row = rows[0]
        for fname in self.REPORT_FIELDS:
            self.assertIn(fname, row, f"{fname} is missing from the report.")

    def test_report_fields_are_groupable(self):
        """Every field the module adds must be usable as a groupby."""
        Report = self.env["purchase.report"]
        for fname in self.REPORT_FIELDS:
            groups = Report._read_group(self._report_domain(), [fname], ["__count"])
            self.assertTrue(
                groups, f"Grouping the purchase analysis by {fname} returned nothing."
            )

    def test_report_values(self):
        """The report must carry the same values as the purchase order line."""
        row = self.env["purchase.report"].search_read(
            self._report_domain(), self.REPORT_FIELDS
        )[0]
        line = self.line

        self.assertEqual(row["fiscal_operation_id"][0], line.fiscal_operation_id.id)
        self.assertEqual(
            row["fiscal_operation_line_id"][0], line.fiscal_operation_line_id.id
        )
        self.assertEqual(row["cfop_id"][0], line.cfop_id.id)
        self.assertEqual(row["fiscal_type"], line.fiscal_type)
        self.assertEqual(row["ncm_id"][0], line.ncm_id.id)
        self.assertFalse(row["nbm_id"])
        self.assertFalse(row["cest_id"])

        # The taxes are really computed on the line, so the comparison below
        # is not a trivial 0 == 0.
        self.assertGreater(line.icms_value, 0.0)
        self.assertGreater(line.ipi_value, 0.0)
        self.assertAlmostEqual(row["icms_value"], line.icms_value, 2)
        self.assertAlmostEqual(row["icmsst_value"], line.icmsst_value, 2)
        self.assertAlmostEqual(row["ipi_value"], line.ipi_value, 2)
        self.assertAlmostEqual(row["pis_value"], line.pis_value, 2)
        self.assertAlmostEqual(row["cofins_value"], line.cofins_value, 2)
        self.assertAlmostEqual(row["ii_value"], line.ii_value, 2)
        self.assertAlmostEqual(row["freight_value"], line.freight_value, 2)
        self.assertAlmostEqual(row["insurance_value"], line.insurance_value, 2)
        self.assertAlmostEqual(row["other_value"], line.other_value, 2)

        expected_total = (
            line.price_unit / (self.order.currency_rate or 1.0) * line.product_qty
            + (line.ipi_value or 0.0)
            + (line.icmsst_value or 0.0)
            + (line.freight_value or 0.0)
            + (line.insurance_value or 0.0)
            + (line.other_value or 0.0)
        )
        self.assertAlmostEqual(row["total_with_taxes"], expected_total, 2)
