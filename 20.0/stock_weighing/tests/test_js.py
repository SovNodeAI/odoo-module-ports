# Copyright 2026 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from urllib.parse import urlencode

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestStockWeighingJs(HttpCase):
    def test_js(self):
        test_filter = urlencode({"filter": "@stock_weighing/"})
        self.browser_js(
            "/web/tests?headless&loglevel=2&preset=desktop&timeout=15000&"
            + test_filter,
            "",
            "",
            login="admin",
            timeout=1800,
            success_signal="[HOOT] Test suite succeeded",
            error_checker=lambda x: "[HOOT]" not in x,
        )
