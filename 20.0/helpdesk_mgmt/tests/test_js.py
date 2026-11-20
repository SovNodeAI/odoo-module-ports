# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import odoo

from odoo.addons.web.tests.test_js import unit_test_error_checker


@odoo.tests.tagged("hoot", "post_install", "-at_install")
class TestHelpdesMgmtJs(odoo.tests.HttpCase):
    """Run the module's own JavaScript unit tests (static/tests) in the browser.

    Odoo 20's WebSuite is a cross-module suite: a subclass of it is picked up
    for other modules' test runs as well. This class only opens the module's
    own hoot suite. It keeps the "hoot" tag WebSuite carries, so a run with
    "-hoot" skips it as before.
    """

    @staticmethod
    def _hoot_id(name):
        """The id hoot gives a suite: a hash of its full name (the computation
        of ``_generate_hash`` in ``addons/web/tests/test_js.py``)."""
        value = 0
        for char in name:
            value = ((value << 5) - value + ord(char)) & 0xFFFFFFFF
        return f"{value:08x}"

    @odoo.tests.no_retry
    def test_helpdesk_mgmt(self):
        suite = self._hoot_id("@helpdesk_mgmt")
        self.browser_js(
            f"/web/tests?headless&loglevel=2&preset=desktop&timeout=15000&id={suite}",
            "",
            "",
            login="admin",
            timeout=1800,
            success_signal="[HOOT] Test suite succeeded",
            error_checker=unit_test_error_checker,
        )
