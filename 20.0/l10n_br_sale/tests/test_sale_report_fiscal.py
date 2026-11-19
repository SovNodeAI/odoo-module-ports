# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged

from .tools import load_sale_fixture_files

# Every field this module adds to the sales analysis report.
REPORT_FIELDS = [
    "fiscal_operation_id",
    "fiscal_operation_line_id",
    "ind_pres",
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


@tagged("post_install", "-at_install")
class TestSaleReportFiscal(TransactionCase):
    """The Brazilian fiscal columns have to reach the sales analysis.

    Odoo 20 builds sale.report from _select_dict()/_groupby_list() and fills a
    field it does not find in the dictionary with NULL, so a module that still
    extends _select_additional_fields()/_group_by_sale() installs and passes
    while its columns stay empty.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        if not cls.env.ref(
            "l10n_br_sale.main_so_only_products", raise_if_not_found=False
        ):
            load_sale_fixture_files(cls.env)
        cls.order = cls.env.ref("l10n_br_sale.main_so_only_products")
        cls.lines = cls.order.order_line.filtered(lambda line: not line.display_type)
        cls.env.flush_all()

    def _report_rows(self):
        return self.env["sale.report"].search([("name", "=", self.order.name)])

    def test_sale_report_reads_every_fiscal_field(self):
        """search_read has to return every field the module adds."""
        rows = self._report_rows()
        self.assertTrue(rows, "The sale order lines are missing from sale.report")
        values = rows.search_read(
            [("name", "=", self.order.name)], REPORT_FIELDS
        )
        self.assertEqual(len(values), len(rows))
        for value in values:
            self.assertEqual(set(value), set(REPORT_FIELDS) | {"id"})

    def test_sale_report_groups_by_every_fiscal_field(self):
        """_read_group has to accept every field the module adds."""
        for fname in REPORT_FIELDS:
            groups = self.env["sale.report"]._read_group(
                [("name", "=", self.order.name)], [fname], ["__count"]
            )
            self.assertTrue(groups, f"No group returned for {fname}")
            self.assertEqual(
                sum(count for _value, count in groups),
                len(self.lines),
                f"Wrong number of lines grouped by {fname}",
            )

    def test_sale_report_fiscal_values(self):
        """The report has to carry the fiscal values of the sale order lines."""
        rows = self._report_rows()
        self.assertTrue(rows)
        for row in rows:
            line = self.lines.filtered(lambda ln, row=row: ln.product_id == row.product_id)
            self.assertEqual(len(line), 1)
            self.assertEqual(row.fiscal_operation_id, line.fiscal_operation_id)
            self.assertEqual(
                row.fiscal_operation_line_id, line.fiscal_operation_line_id
            )
            self.assertEqual(row.cfop_id, line.cfop_id)
            self.assertEqual(row.fiscal_type, line.fiscal_type)
            self.assertEqual(row.ncm_id, line.ncm_id)
            self.assertEqual(row.nbm_id, line.nbm_id)
            self.assertEqual(row.cest_id, line.cest_id)
            self.assertEqual(row.ind_pres, self.order.ind_pres)
            self.assertAlmostEqual(row.icms_value, line.icms_value, 2)
            self.assertAlmostEqual(row.icmsst_value, line.icmsst_value, 2)
            self.assertAlmostEqual(row.ipi_value, line.ipi_value, 2)
            self.assertAlmostEqual(row.pis_value, line.pis_value, 2)
            self.assertAlmostEqual(row.cofins_value, line.cofins_value, 2)
            self.assertAlmostEqual(row.ii_value, line.ii_value, 2)
            self.assertAlmostEqual(row.freight_value, line.freight_value, 2)
            self.assertAlmostEqual(row.insurance_value, line.insurance_value, 2)
            self.assertAlmostEqual(row.other_value, line.other_value, 2)
            # total_with_taxes = price_total converted to the company currency
            # plus the taxes and costs that are not part of price_total.
            expected = (
                line.price_total / (self.order.currency_rate or 1.0)
                + line.ipi_value
                + line.icmsst_value
                + line.freight_value
                + line.insurance_value
                + line.other_value
            )
            self.assertAlmostEqual(row.total_with_taxes, expected, 2)
