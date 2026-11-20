# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import odoo

from odoo.addons.web.tests.test_js import WebSuite


@odoo.tests.tagged("post_install", "-at_install")
class TestAutomationOCA(WebSuite):
    """Test Automation OCA"""

    def test_automation_oca(self, modules):
        self._test_params = [("+", "@automation_oca")]
        self.test_unit_desktop(modules)
