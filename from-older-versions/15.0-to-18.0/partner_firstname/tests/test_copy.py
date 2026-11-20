# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Test copy function for models."""
from odoo.tests import TransactionCase

from .base import MailInstalled


class UserCase(TransactionCase, MailInstalled):
    """Test ``res.users``."""

    def setUp(self):
        super(UserCase, self).setUp()
        self.create_original()

    def create_original(self):
        self.original = self.env["res.users"].create(
            {
                "firstname": "Firstname",
                "lastname": "Lastname",
                "name": "Firstname Lastname",
                "login": "firstname.lastname",
            }
        )

    def tearDown(self):
        super(UserCase, self).tearDown()

    def compare(self, copy):
        self.assertEqual(copy.lastname, "Lastname2")
        self.assertEqual(copy.firstname, "Firstname2")
        self.assertEqual(copy.name, "Firstname2 Lastname2")

    def test_copy_name(self):
        """Copy original with default name set - firstname lastname not set."""
        copy = self.original.copy({"name": "Firstname2 Lastname2"})
        self.compare(copy)

    def test_copy_firstname_lastname(self):
        """Copy original with default firstname and lastname set"""
        copy = self.original.copy({"firstname": "Firstname2", "lastname": "Lastname2"})
        self.compare(copy)

    def test_copy_firstname_lastname_name(self):
        """Copy original with default firstname, lastname and name set"""
        copy = self.original.copy(
            {
                "firstname": "Firstname2",
                "lastname": "Lastname2",
                "name": "Firstname2 Lastname2",
            }
        )
        self.compare(copy)

    def test_copy_firstname_only(self):
        """Copy with only a firstname: the lastname is not pulled from name."""
        copy = self.original.copy({"firstname": "Firstname2", "lastname": False})
        self.assertEqual(copy.firstname, "Firstname2")
        self.assertEqual(copy.lastname, False)
        self.assertEqual(copy.name, "Firstname2")

    def test_copy_user_firstname_only(self):
        """A user copied with only a firstname keeps the lastname empty."""
        copy = self.original.copy({"firstname": "Firstname2", "lastname": False})
        self.assertEqual(copy.firstname, "Firstname2")
        self.assertEqual(copy.lastname, False)
        self.assertEqual(copy.name, "Firstname2")


class PartnerMultiWordCase(TransactionCase):
    """Copying a partner with multi-word names keeps the split fields."""

    def test_copy_multiword_lastname(self):
        partner = self.env["res.partner"].create(
            {"firstname": "Jean Luc", "lastname": "Picard"}
        )
        copy = partner.copy()
        self.assertEqual(copy.firstname, "Jean Luc")
        self.assertEqual(copy.lastname, "Picard (copy)")
        self.assertEqual(copy.name, "Jean Luc Picard (copy)")

    def test_copy_multiword_firstname(self):
        partner = self.env["res.partner"].create(
            {"firstname": "Federico", "lastname": "García Lorca"}
        )
        copy = partner.copy()
        self.assertEqual(copy.firstname, "Federico")
        self.assertEqual(copy.lastname, "García Lorca (copy)")

    def test_copy_changes_company_type(self):
        """Copying a person as a company stores the whole name in lastname."""
        partner = self.env["res.partner"].create(
            {"firstname": "Federico", "lastname": "García Lorca"}
        )
        copy = partner.copy({"is_company": True})
        self.assertTrue(copy.is_company)
        self.assertEqual(copy.firstname, False)
        self.assertEqual(copy.lastname, "Federico García Lorca (copy)")

    def test_copy_explicit_empty_name(self):
        """``name=False`` in the defaults still gets the ``(copy)`` suffix."""
        partner = self.env["res.partner"].create(
            {"firstname": "Ada", "lastname": "Lovelace"}
        )
        copy = partner.copy({"name": False})
        self.assertEqual(copy.firstname, "Ada")
        self.assertEqual(copy.lastname, "Lovelace (copy)")

    def test_copy_multiple_partners(self):
        """The list view duplicates several partners at once."""
        partners = self.env["res.partner"].create(
            [
                {"firstname": "Ada", "lastname": "Lovelace"},
                {"firstname": "Alan", "lastname": "Turing"},
            ]
        )
        copies = partners.copy()
        self.assertEqual(len(copies), 2)
        self.assertEqual(copies[0].lastname, "Lovelace (copy)")
        self.assertEqual(copies[1].lastname, "Turing (copy)")
