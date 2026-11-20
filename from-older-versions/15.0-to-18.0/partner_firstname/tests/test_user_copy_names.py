# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestUserCopyKeepsNames(TransactionCase):
    def test_duplicate_user_with_two_word_first_name(self):
        """Duplicating a user does not move part of the first name into the last name."""
        user = self.env["res.users"].create(
            {"firstname": "Jean Luc", "lastname": "Picard", "login": "jl.picard"}
        )
        self.assertEqual(self.env["res.partner"]._get_names_order(), "first_last")
        copy = user.copy()
        self.assertEqual(copy.firstname, "Jean Luc")
        self.assertEqual(copy.lastname, "Picard (copy)")
        self.assertEqual(copy.name, "Jean Luc Picard (copy)")

    def test_duplicate_user_with_a_given_name(self):
        """A name given for the copy is still split the usual way."""
        user = self.env["res.users"].create(
            {"firstname": "Jean Luc", "lastname": "Picard", "login": "jl.picard2"}
        )
        copy = user.copy({"name": "William Riker", "login": "w.riker"})
        self.assertEqual(copy.firstname, "William")
        self.assertEqual(copy.lastname, "Riker")
