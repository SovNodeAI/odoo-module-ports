# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestOwnPreference(TransactionCase):
    def test_user_changes_own_preference(self):
        """A plain internal user may change this preference on their own user record.
        In Odoo 20 that takes user_writeable=True on the field."""
        user = new_test_user(self.env, login="own_preference_user", groups="base.group_user")
        user.with_user(user).write({"technical_features": True})
        self.assertTrue(user.has_group("base_technical_features.group_technical_features"))
