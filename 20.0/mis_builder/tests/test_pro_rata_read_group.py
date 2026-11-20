# Copyright 2025 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.orm.model_classes import add_to_registry
from odoo.tests import TransactionCase


class TestProrataReadGroup(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from .fake_models import ProrataReadGroupThing

        add_to_registry(cls.registry, ProrataReadGroupThing)
        model_name = "prorata.read.group.thing"
        cls.registry._setup_models__(cls.env.cr, [model_name])
        cls.registry.init_models(cls.env.cr, [model_name], {"models_to_check": True})
        cls.addClassCleanup(cls.registry.__delitem__, model_name)

        cls.thing_model = cls.env["prorata.read.group.thing"]
        cls.thing_model.create(
            {
                "date_from": "2024-01-01",
                "date_to": "2024-01-05",
                "account_code": "A1",
                "debit": 7,
                "credit": 0,
            }
        )
        cls.thing_model.create(
            {
                "date_from": "2024-01-01",
                "date_to": "2024-01-20",
                "account_code": "A1",
                "debit": 200,
                "credit": 0,
            }
        )
        cls.thing_model.create(
            {
                "date_from": "2024-01-15",
                "date_to": "2024-01-20",
                "account_code": "A1",
                "debit": 11,
                "credit": 0,
            }
        )

    def test_prorata_formatted_read_group(self):
        """Test a pro-rata formatted_read_group with a date period."""
        data = self.thing_model.formatted_read_group(
            [("date", ">=", "2024-01-11"), ("date", "<=", "2024-01-20")],
            aggregates=["debit:sum", "credit:sum"],
            groupby=["account_code", "company_id"],
        )[0]
        self.assertEqual(data["debit:sum"], 111)
        self.assertEqual(data["credit:sum"], 0)
        self.assertEqual(data["account_code"], "A1")
        self.assertEqual(
            data["company_id"], (self.env.company.id, self.env.company.name)
        )

    def test_formatted_read_group(self):
        """Test a regular formatted_read_group without date filtering still works."""
        data = self.thing_model.formatted_read_group(
            domain=[],
            groupby=["account_code", "company_id"],
            aggregates=["debit:sum", "credit:sum"],
        )[0]
        self.assertEqual(data["debit:sum"], 218)
        self.assertEqual(data["credit:sum"], 0)
        self.assertEqual(data["account_code"], "A1")
        self.assertEqual(
            data["company_id"], (self.env.company.id, self.env.company.name)
        )

    def test_prorata_read_group_internal(self):
        """Test a regular _read_group without date filtering still works."""
        data = self.thing_model._read_group(
            domain=[("date", ">=", "2024-01-11"), ("date", "<=", "2024-01-20")],
            groupby=["account_code", "company_id"],
            aggregates=["debit:sum", "credit:sum"],
        )
        self.assertEqual(
            data,
            [
                ("A1", self.env.company, 111, 0),
            ],
        )

    def test_read_group_internal(self):
        """Test a regular _read_group without date filtering still works."""
        data = self.thing_model._read_group(
            domain=[],
            groupby=["account_code", "company_id"],
            aggregates=["debit:sum", "credit:sum"],
        )
        self.assertEqual(
            data,
            [
                ("A1", self.env.company, 218, 0),
            ],
        )

    def test_mis_report_query_stored_fields(self):
        self.thing_model.create(
            [
                {
                    "date_from": "2024-02-01",
                    "date_to": "2024-02-29",
                    "account_code": "QUERY",
                    "debit": 12,
                    "credit": 2,
                },
                {
                    "date_from": "2024-02-02",
                    "date_to": "2024-02-29",
                    "account_code": "QUERY",
                    "debit": 24,
                    "credit": 6,
                },
            ]
        )
        model = self.env["ir.model"].search(
            [("model", "=", self.thing_model._name)]
        )
        fields = self.env["ir.model.fields"].search(
            [("model_id", "=", model.id), ("name", "in", ("debit", "credit"))]
        )
        date_field = self.env["ir.model.fields"].search(
            [("model_id", "=", model.id), ("name", "=", "date_from")]
        )
        query_ids = []
        for aggregate in ("sum", "avg", "min", "max"):
            for prefix, account_code in (("stored", "QUERY"), ("empty", "NO_DATA")):
                query_ids.append(
                    (
                        0,
                        0,
                        {
                            "name": f"{prefix}_{aggregate}",
                            "model_id": model.id,
                            "field_ids": [(6, 0, fields.ids)],
                            "date_field": date_field.id,
                            "aggregate": aggregate,
                            "domain": repr([("account_code", "=", account_code)]),
                        },
                    )
                )
        report = self.env["mis.report"].create(
            {"name": "Stored field aggregates", "query_ids": query_ids}
        )
        result = report.evaluate(
            report._prepare_aep(self.env.company), "2024-02-01", "2024-02-29"
        )
        expected = {
            "sum": {"debit": 36, "credit": 8},
            "avg": {"debit": 18, "credit": 4},
            "min": {"debit": 12, "credit": 2},
            "max": {"debit": 24, "credit": 6},
        }
        for aggregate, expected_values in expected.items():
            with self.subTest(aggregate=aggregate):
                for prefix in ("stored", "empty"):
                    data = result[f"{prefix}_{aggregate}"]
                    self.assertEqual(data.count, 2 if prefix == "stored" else 0)
                    for field_name in ("debit", "credit"):
                        value = getattr(data, field_name)
                        if prefix == "stored":
                            self.assertEqual(value, expected_values[field_name])
                        elif aggregate == "sum":
                            # summed in SQL: the empty value of _read_group,
                            # as on 19.0, where read_group returned the same
                            self.assertIs(value, False)
                        else:
                            # min, max and avg are computed in Python
                            self.assertIsNone(value)
