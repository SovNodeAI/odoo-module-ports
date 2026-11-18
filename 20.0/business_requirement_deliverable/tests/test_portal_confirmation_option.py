# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPortalConfirmationOption(TransactionCase):
    def test_option_is_read_from_the_system_parameter(self):
        """The portal page asks which confirmation the customer may give. Odoo 20
        reads a text parameter with get_str; get_param no longer exists."""
        requirement = self.env["business.requirement"]
        key = "business_requirement_deliverable.br_portal_confirmation_options"
        parameters = self.env["ir.config_parameter"].sudo()
        parameters.search([("key", "=", key)]).unlink()
        self.assertEqual(requirement.get_portal_confirmation_action(), "none")
        parameters.set_str(key, "sign")
        self.assertEqual(requirement.get_portal_confirmation_action(), "sign")
