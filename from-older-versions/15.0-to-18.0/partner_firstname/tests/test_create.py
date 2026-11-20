# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L. - Jairo Llopis.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""Test default values for models."""

from odoo.tests import TransactionCase

from .base import MailInstalled


class PersonCase(TransactionCase):
    """Test ``res.partner`` when it is a person."""

    allow_inherited_tests_method = True

    context = {"default_is_company": False}
    model = "res.partner"

    def setUp(self):
        super(PersonCase, self).setUp()
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

        super(PersonCase, self).tearDown()

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


class ExplicitSplitFieldsCase(TransactionCase):
    """The split fields given by the caller win over the full name."""

    def test_create_with_firstname_and_name(self):
        """A contact created with firstname and name is not duplicated."""
        partner = self.env["res.partner"].create(
            {"firstname": "Alice", "name": "Alice"}
        )
        self.assertEqual(partner.firstname, "Alice")
        self.assertEqual(partner.lastname, False)
        self.assertEqual(partner.name, "Alice")

    def test_create_with_lastname_and_name(self):
        """A contact created with lastname and name is not duplicated."""
        partner = self.env["res.partner"].create(
            {"lastname": "García Lorca", "name": "García Lorca"}
        )
        self.assertEqual(partner.lastname, "García Lorca")
        self.assertEqual(partner.firstname, False)
        self.assertEqual(partner.name, "García Lorca")

    def test_create_person_with_default_is_company(self):
        """An explicit ``company_type`` wins over ``default_is_company``.

        The Customers and Vendors actions put ``default_is_company`` in the
        context; a contact created from them must still be split as a person.
        """
        partner = (
            self.env["res.partner"]
            .with_context(default_is_company=True)
            .create({"company_type": "person", "name": "Federico García Lorca"})
        )
        self.assertFalse(partner.is_company)
        self.assertEqual(partner.firstname, "Federico")
        self.assertEqual(partner.lastname, "García Lorca")


class CompanyCase(PersonCase):
    """Test ``res.partner`` when it is a company."""

    context = {"default_is_company": True}

    def setUp(self):
        super(CompanyCase, self).setUp()
        self.good_values.update(lastname=self.values["name"], firstname=False)
        self.values = self.good_values.copy()


class UserCase(PersonCase, MailInstalled):
    """Test ``res.users``."""

    model = "res.users"
    context = {"default_login": "user@example.com"}

    def tearDown(self):
        # Cannot create users if ``mail`` is installed
        if self.mail_installed():
            # Skip tests
            super(PersonCase, self).tearDown()
        else:
            # Run tests
            super(UserCase, self).tearDown()
