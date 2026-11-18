# Copyright 2015 Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""These tests try to mimic the behavior of the UI form.

The form operates in onchange mode, with its limitations.
"""

from psycopg2 import IntegrityError

from odoo.tests import Form, TransactionCase
from odoo.tools import mute_logger


class PartnerCompanyCase(TransactionCase):
    is_company = True

    def get_form(self, view=None):
        """Return a form for a new partner of the case's company type.

        Since Odoo 20, ``is_company`` is a computed field (a partner is a
        company when it is its own commercial entity and has a Tax ID), hence
        the Tax ID is set on the company case for the partner to be one.
        """
        partner = self.env["res.partner"].with_context(
            default_is_company=self.is_company,
            default_vat=self.is_company and "BE0477472701" or False,
        )
        return Form(partner, view=view)

    def test_create_from_form(self):
        name = "Sôme company"
        with self.get_form() as partner_form:
            partner_form.name = name

        self.assertEqual(partner_form.name, name)
        self.assertEqual(partner_form.firstname, False)
        self.assertEqual(partner_form.lastname, name)

    def test_create_from_form_keeps_name_over_default_name(self):
        """If the name is updated in the create dialog, it must be saved instead of the
        search term
        """
        with Form(
            self.env["res.partner"].with_context(
                default_name="Test",
                default_is_company=True,
                default_vat="BE0477472701",
            )
        ) as partner_form:
            partner_form.name = "Full Test"

        self.assertEqual(partner_form.name, "Full Test")
        self.assertEqual(partner_form.firstname, False)
        self.assertEqual(partner_form.lastname, "Full Test")

    def test_empty_name(self):
        """If we empty the name and save the form, the core constraint on
        the name must be raised (firstname and lastname are reset...)
        """
        with self.get_form(view="base.view_partner_form") as partner_form:
            name = "Foó"
            # User sets a name
            partner_form.name = name
            # call save to  trigger the inverse
            partner_form.save()
            self.assertEqual(partner_form.name, name)
            self.assertEqual(partner_form.firstname, False)
            self.assertEqual(partner_form.lastname, name)

            # User unsets name
            partner_form.name = ""
            # call save to  trigger the inverse and therefore raise an exception
            with (
                self.assertRaises(IntegrityError),
                mute_logger("odoo.sql_db"),
                self.env.cr.savepoint(),
            ):
                partner_form.save()

            name += " bis"
            partner_form.name = name
            partner_form.save()
            self.assertEqual(partner_form.name, name)
            self.assertEqual(partner_form.firstname, False)

            # assert below will fail until merge of
            #   https://github.com/odoo/odoo/pull/45355
            # self.assertEqual(partner_form.lastname, name)


class PartnerContactCase(TransactionCase):
    is_company = False

    def get_form(self, view=None):
        """Return a form for a new partner of the case's company type.

        Since Odoo 20, ``is_company`` is a computed field (a partner is a
        company when it is its own commercial entity and has a Tax ID), hence
        the Tax ID is set on the company case for the partner to be one.
        """
        partner = self.env["res.partner"].with_context(
            default_is_company=self.is_company,
            default_vat=self.is_company and "BE0477472701" or False,
        )
        return Form(partner, view=view)

    def test_create_from_form_only_firstname(self):
        """A user creates a contact with only the firstname from the form."""
        firstname = "Fïrst"
        with self.get_form() as partner_form:
            # Changes firstname, which triggers compute
            partner_form.firstname = firstname

        self.assertEqual(partner_form.lastname, False)
        self.assertEqual(partner_form.firstname, firstname)
        self.assertEqual(partner_form.name, firstname)

    def test_create_from_form_only_lastname(self):
        """A user creates a contact with only the lastname from the form."""
        lastname = "Läst"
        with self.get_form() as partner_form:
            # Changes lastname, which triggers compute
            partner_form.lastname = lastname

        self.assertEqual(partner_form.firstname, False)
        self.assertEqual(partner_form.lastname, lastname)
        self.assertEqual(partner_form.name, lastname)

    def test_create_from_form_all(self):
        """A user creates a contact with all names from the form."""
        firstname = "Fïrst"
        lastname = "Läst"
        with self.get_form() as partner_form:
            # Changes firstname, which triggers compute
            partner_form.firstname = firstname

            # Changes lastname, which triggers compute
            partner_form.lastname = lastname

        self.assertEqual(partner_form.lastname, lastname)
        self.assertEqual(partner_form.firstname, firstname)
        self.assertEqual(partner_form.name, " ".join((firstname, lastname)))
