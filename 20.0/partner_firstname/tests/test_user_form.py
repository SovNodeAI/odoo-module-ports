# Copyright 2016 Yannick Vaucher (Camptocamp SA)
# Copyright 2020 Therp BV - https://therp.nl.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from lxml import etree

from odoo.tests import Form, TransactionCase


class UserOnchangeCase(TransactionCase):
    def test_create_from_form_only_firstname(self):
        """In a new users form, a user set only the firstname."""
        login = "Zoë"
        firstname = "Zoë"
        with self.get_user_form() as user_form:
            user_form.login = login
            # Changes firstname, which triggers onchanges
            user_form.firstname = firstname

        self.assertEqual(user_form.lastname, False)
        self.assertEqual(user_form.firstname, firstname)
        self.assertEqual(user_form.name, firstname)

    def test_create_from_form_only_lastname(self):
        """In a new user form, a user set only the lastname."""
        login = "Żywioł"
        lastname = "Żywioł"
        with self.get_user_form() as user_form:
            user_form.login = login
            # Changes lastname, which triggers onchanges
            user_form.lastname = lastname

        self.assertEqual(user_form.firstname, False)
        self.assertEqual(user_form.lastname, lastname)
        self.assertEqual(user_form.name, lastname)

    def test_create_from_form_all(self):
        """In a new user form, a user set all names."""
        login = "Zoë.Żywioł"
        firstname = "Zoë"
        lastname = "Żywioł"
        with self.get_user_form() as user_form:
            user_form.login = login
            # Changes firstname, which triggers onchanges
            user_form.firstname = firstname
            # Changes lastname, which triggers onchanges
            user_form.lastname = lastname

        self.assertEqual(user_form.lastname, lastname)
        self.assertEqual(user_form.firstname, firstname)
        self.assertEqual(user_form.name, " ".join((firstname, lastname)))

    def get_user_form(self):
        return Form(self.env["res.users"], view="partner_firstname.view_users_form")


class TestNameFieldsAlwaysShown(TransactionCase):
    """The first-name and last-name fields must not sit inside a part of the form
    that Odoo hides under a condition of its own: the name itself is read-only."""

    def _foreign_conditions(self, model, view_xmlid, path):
        view = self.env.ref(view_xmlid)
        arch = etree.fromstring(self.env[model].get_view(view.id, "form")["arch"])
        nodes = arch.xpath(path)
        self.assertTrue(nodes, path)
        found = []
        for node in nodes:
            for parent in node.iterancestors():
                condition = parent.get("invisible")
                # the module's own rule (names are for people, not companies) is fine
                if condition and condition not in ("is_company",):
                    found.append((parent.tag, parent.get("name"), condition))
                if parent.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                    found.append((parent.tag, parent.get("name"), "heading"))
        return found

    def test_user_form(self):
        self.assertEqual(
            self._foreign_conditions(
                "res.users", "base.view_users_form", "//field[@name='firstname']"
            ),
            [],
        )

    def test_contact_sub_form(self):
        self.assertEqual(
            self._foreign_conditions(
                "res.partner",
                "base.view_partner_form",
                "//field[@name='child_ids']/form//field[@name='firstname']",
            ),
            [],
        )
