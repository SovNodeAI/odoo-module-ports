# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import odoo.tests
from odoo.fields import Command


@odoo.tests.tagged("post_install", "-at_install")
class BusinessRequirementDeliverablePortal(odoo.tests.HttpCase):
    def setUp(self):
        super().setUp()
        # Demo data is not installed on the test database: create the portal
        # user the tour logs in with.
        self.env["ir.config_parameter"].sudo().set_int(
            "auth_password_policy.minlength", 4
        )
        self.partner_portal = self.env["res.partner"].create(
            {"name": "Joel Willis", "email": "joel.willis63@example.com"}
        )
        self.user_portal = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "login": "portal",
                    "password": "portal",
                    "partner_id": self.partner_portal.id,
                    "group_ids": [
                        Command.set([self.env.ref("base.group_portal").id])
                    ],
                }
            )
        )
        self.br = self.env["business.requirement"].create(
            {"description": "test", "portal_published": True}
        )
        self.brd = self.env["business.requirement.deliverable"].create(
            {
                "name": "test",
                "portal_published": True,
                "business_requirement_id": self.br.id,
            }
        )
        # Subscribe the requirement, not the deliverable: the portal counter
        # filters on the requirement's followers, and message_subscribe()
        # propagates them down to its deliverable_lines (not the other way
        # around), which is what makes the /my/brd entry visible.
        self.br.message_subscribe(partner_ids=self.partner_portal.ids)

    def test_tour(self):
        self.start_tour(
            "/", "business_requirement_deliverable_portal_tour", login="portal"
        )

    def test_portal_brd_page_renders_chatter(self):
        """The deliverable portal page must render, including its chatter.

        Odoo 20's portal.message_thread reads its values from the t-call
        attributes (object, token, pid, hash); a t-set child of the t-call is
        no longer forwarded, so the page used to fail with KeyError: 'object'.
        """
        self.authenticate("portal", "portal")
        response = self.url_open(f"/my/brd/{self.brd.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("o_portal_chatter", response.text)
        self.assertIn(
            'data-res_model="business.requirement.deliverable"', response.text
        )
        self.assertIn(f'data-res_id="{self.brd.id}"', response.text)
