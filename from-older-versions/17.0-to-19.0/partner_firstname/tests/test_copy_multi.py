# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Test multi-record duplication and duplicated values in Odoo 19."""
from odoo.tests.common import TransactionCase


class CopyMultiCase(TransactionCase):
    def order_set(self, order):
        self.env["ir.config_parameter"].sudo().set_param("partner_names_order", order)

    def test_copy_single_person(self):
        """A single duplication keeps the 17.0 name-copying behaviour."""
        original = self.env["res.partner"].create(
            {"firstname": "Alice", "lastname": "Example"}
        )
        self.assertRecordValues(
            original.copy(),
            [
                {
                    "firstname": "Alice",
                    "lastname": "Example (copy)",
                    "name": "Alice Example (copy)",
                }
            ],
        )

    def test_copy_multiple_partners(self):
        """One duplication call handles people and companies in every name order."""
        original_person = self.env["res.partner"].create(
            {"firstname": "Alice", "lastname": "Example"}
        )
        original_company = self.env["res.partner"].create(
            {"name": "ACME Ltd", "is_company": True}
        )
        cases = {
            "first_last": {
                "firstname": "Alice",
                "lastname": "Example (copy)",
                "name": "Alice Example (copy)",
            },
            "last_first": {
                "firstname": "Alice (copy)",
                "lastname": "Example",
                "name": "Example Alice (copy)",
            },
            "last_first_comma": {
                "firstname": "Alice (copy)",
                "lastname": "Example",
                "name": "Example, Alice (copy)",
            },
        }
        for order, expected_person in cases.items():
            with self.subTest(order=order):
                self.order_set(order)
                copies = (original_person | original_company).copy()
                self.assertRecordValues(
                    copies,
                    [
                        expected_person,
                        {
                            "firstname": False,
                            "lastname": "ACME Ltd (copy)",
                            "name": "ACME Ltd (copy)",
                        },
                    ],
                )

    def test_create_company_from_default(self):
        """Related Company quick-create keeps its whole company name."""
        partner = (
            self.env["res.partner"]
            .with_context(default_is_company=True)
            .create({"name": "ACME Ltd"})
        )
        self.assertTrue(partner.is_company)
        self.assertEqual(partner.name, "ACME Ltd")
        self.assertEqual(partner.lastname, "ACME Ltd")
        self.assertFalse(partner.firstname)

    def test_company_copy_data_is_ready_to_create(self):
        """A caller that creates from copy_data() gets the copied company name."""
        company = self.env["res.partner"].create(
            {"name": "ACME Ltd", "is_company": True}
        )
        vals = company.copy_data()[0]
        name = vals["name"]
        self.assertNotEqual(name, company.name)
        self.assertEqual(vals["lastname"], name)
        self.assertFalse(vals["firstname"])
        # create() takes the name out of the values it is given
        copy = self.env["res.partner"].create(dict(vals))
        self.assertRecordValues(
            copy, [{"firstname": False, "lastname": name, "name": name}]
        )
