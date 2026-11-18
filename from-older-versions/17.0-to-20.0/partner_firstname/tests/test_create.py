# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L. - Jairo Llopis.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""Test default values for models."""

from odoo.tests.common import TransactionCase

from .base import MailInstalled


class PersonCase(TransactionCase):
    """Test ``res.partner`` when it is a person."""

    # Since Odoo 18 the test loader only runs methods written in a class body,
    # unless this flag lets the inherited test methods run too.
    allow_inherited_tests_method = True

    context = {"default_is_company": False}
    model = "res.partner"

    def setUp(self):
        super().setUp()
        self.good_values = {"firstname": "Núñez", "lastname": "Fernán"}
        self.good_values["name"] = "{} {}".format(
            self.good_values["firstname"], self.good_values["lastname"]
        )
        if "default_is_company" in self.context:
            self.good_values["is_company"] = self.context["default_is_company"]
        self.values = self.good_values.copy()

    def tearDown(self):
        self.record = (
            self.env[self.model].with_context(**self.context).create(self.values)
        )
        for key, value in self.good_values.items():
            self.assertEqual(self.record[key], value, "Checking key %s" % key)

        super().tearDown()

    def test_no_name(self):
        """Name is calculated."""
        del self.values["name"]

    def test_wrong_name_value(self):
        """Wrong name value is ignored, name is calculated."""
        self.values["name"] = "BÄD"

    def test_wrong_name_context(self):
        """Wrong name context is ignored, name is calculated."""
        del self.values["name"]
        self.context["default_name"] = "BÄD"

    def test_wrong_name_value_and_context(self):
        """Wrong name value and context is ignored, name is calculated."""
        self.values["name"] = "BÄD1"
        self.context["default_name"] = "BÄD2"


class CompanyCase(PersonCase):
    """Test ``res.partner`` when it is a company."""

    # Since Odoo 18, ``is_company`` is computed: a partner is a company when it
    # is its own commercial entity and has a Tax ID, hence the Tax ID here.
    context = {"default_is_company": True, "default_vat": "BE0477472701"}

    def setUp(self):
        super().setUp()
        self.good_values.update(
            lastname=self.values["name"], firstname=False, vat="BE0477472701"
        )
        self.values = self.good_values.copy()


class UserCase(PersonCase, MailInstalled):
    """Test ``res.users``."""

    model = "res.users"
    context = {"default_login": "user@example.com"}

    def tearDown(self):
        # Cannot create users if ``mail`` is installed
        if self.mail_installed():
            # Skip tests
            super().tearDown()
        else:
            # Run tests
            super().tearDown()
