# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import users
from odoo.tools import mute_logger

from .test_automation_security import TestAutomationSecurity


class TestOrphanRecordsStay(TestAutomationSecurity):
    @users("user_automation_01")
    @mute_logger("odoo.addons.automation_oca.models.automation_record")
    def test_orphan_record_is_still_listed_once_stored(self):
        """A record whose target was deleted stays visible to the Settings group.

        The first search after the deletion marks it as an orphan and empties
        its res_id; once that is stored, later searches must still return it.
        """
        self.env.user.group_ids = [(4, self.env.ref("base.group_system").id)]
        domain = [("configuration_id", "=", self.configuration.id)]
        self.partner_02.unlink()
        record = self.env["automation.record"].search(domain)
        self.assertEqual(len(record), 1)
        self.assertTrue(record.is_orphan_record)
        self.env.flush_all()
        self.env.invalidate_all()
        self.assertEqual(self.env["automation.record"].search(domain), record)
