# Copyright 2015 Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""These tests try to mimic the behavior of the UI form.

The form operates in onchange mode, with its limitations.
"""

from odoo.tests import Form, TransactionCase

from ..exceptions import EmptyNamesError


class PartnerCompanyCase(TransactionCase):
    allow_inherited_tests_method = True

    is_company = True

    def get_form(self, view=None):
        """Return a form for a new partner of the case's company type.

        Odoo 20 replaced the ``company_type`` field with a computed
        ``is_company`` field, which is computed from the Tax ID, so the
        company case also sets a valid Tax ID.
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

    def test_empty_name(self):
        """If we empty the name and save the form, EmptyNamesError must
        be raised (firstname and lastname are reset...)
        """
        with self.get_form(
            view="base.view_partner_form"
        ) as partner_form:

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
            with self.assertRaises(EmptyNamesError), self.env.cr.savepoint():
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
    allow_inherited_tests_method = True

    is_company = False

    def get_form(self, view=None):
        """Return a form for a new partner of the case's company type.

        Odoo 20 replaced the ``company_type`` field with a computed
        ``is_company`` field, which is computed from the Tax ID, so the
        company case also sets a valid Tax ID.
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
