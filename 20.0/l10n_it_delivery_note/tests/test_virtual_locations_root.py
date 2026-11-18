# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestVirtualLocationsRoot(TransactionCase):
    def test_root_is_read_from_and_written_to_the_parameter(self):
        """The root of the virtual locations is kept in a system parameter. Odoo 20
        reads and writes it with get_int / set_int; get_param / set_param are gone."""
        key = "stock.location.virtual_root"
        parameters = self.env["ir.config_parameter"].sudo()
        location = self.env["stock.location"].create(
            {"name": "Virtual root for the test", "usage": "view"}
        )
        parameters.set_int(key, location.id)
        self.assertEqual(
            self.env["stock.location"].get_virtual_locations_root(), location
        )
        # without the parameter, the default of the settings is used and remembered
        parameters.search([("key", "=", key)]).unlink()
        settings = type(self.env["res.config.settings"])
        with patch.object(
            settings, "_default_virtual_locations_root", lambda self: location
        ):
            self.assertEqual(
                self.env["stock.location"].get_virtual_locations_root(), location
            )
        self.assertEqual(parameters.get_int(key), location.id)
