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
        self.values = {"firstname": "Núñez", "lastname": "Fernán"}
        self.values["name"] = "{} {}".format(
            self.values["firstname"], self.values["lastname"]
        )
        if "default_is_company" in self.context:
            self.values["is_company"] = self.context["default_is_company"]

    def tearDown(self):
        for key, value in self.values.items():
            self.assertEqual(self.defaults.get(key), value, "Checking key %s" % key)

        return super(PersonCase, self).tearDown()

    def test_default_get(self):
        """Getting default values for fields includes new fields."""
        self.defaults = (
            self.env[self.model]
            .with_context(self.context, default_name=self.values["name"])
            .default_get(list(self.values.keys()))
        )

class SplitFieldsOnlyCase(TransactionCase):
    """Asking only for the split fields still honours ``default_name``.

    The web client asks for the fields of the view, which do not always
    include ``name``; the split fields must be filled all the same.
    """

    def test_partner_default_get_split_fields_only(self):
        defaults = (
            self.env["res.partner"]
            .with_context(default_name="Fernán Núñez")
            .default_get(["firstname", "lastname"])
        )
        self.assertEqual(defaults.get("firstname"), "Fernán")
        self.assertEqual(defaults.get("lastname"), "Núñez")

    def test_user_default_get_split_fields_only(self):
        defaults = (
            self.env["res.users"]
            .with_context(default_name="Fernán Núñez")
            .default_get(["firstname", "lastname"])
        )
        self.assertEqual(defaults.get("firstname"), "Fernán")
        self.assertEqual(defaults.get("lastname"), "Núñez")


class CompanyCase(PersonCase):
    """Test ``res.partner`` when it is a company."""

    context = {"default_is_company": True}

    def tearDown(self):
        self.values.update(lastname=self.values["name"], firstname=False)
        return super(CompanyCase, self).tearDown()


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
