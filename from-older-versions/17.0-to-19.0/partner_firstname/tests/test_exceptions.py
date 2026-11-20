# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Test the error raised when a partner is left without a name."""
from odoo.tests.common import TransactionCase

from ..exceptions import EmptyNamesError


class EmptyNamesErrorCase(TransactionCase):
    def test_error_uses_record_env(self):
        """The message is translated with the record's env, without warnings."""
        partner = self.env["res.partner"].create(
            {"firstname": "Firstname", "lastname": "Lastname"}
        )
        with self.assertNoLogs("odoo.tools.translate", "WARNING"):
            with self.assertRaises(EmptyNamesError) as error:
                partner.firstname = partner.lastname = False
        self.assertEqual(
            error.exception.args[1], partner.env._("No name is set.")
        )
        self.assertEqual(
            error.exception.args[0],
            partner.env._("Error(s) with partner %d's name.") % partner.id,
        )
