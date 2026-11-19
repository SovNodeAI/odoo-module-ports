# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestBarcodeScannerJs(HttpCase):
    """Run the module's JS unit tests (``static/tests``) in the browser.

    A Chrome/Chromium binary is required: without one the run is skipped, not
    passed.
    """

    @staticmethod
    def _hoot_id(name):
        """The id hoot gives a suite: a hash of its full name (same computation
        as ``_generate_hash`` in ``addons/web/tests/test_js.py``)."""
        value = 0
        for char in name:
            value = ((value << 5) - value + ord(char)) & 0xFFFFFFFF
        return f"{value:08x}"

    def test_js(self):
        # Odoo 20: select the module's own suite by id, as Odoo's WebSuite does.
        # The text filter "BarcodeScanner" also matches tests of Odoo itself.
        suite = self._hoot_id("@barcode_scanner")
        self.browser_js(
            f"/web/tests?headless&loglevel=2&preset=desktop&id={suite}",
            "",
            "",
            login="admin",
            success_signal="[HOOT] Test suite succeeded",
            error_checker=lambda message: "[HOOT]" not in message,
        )
