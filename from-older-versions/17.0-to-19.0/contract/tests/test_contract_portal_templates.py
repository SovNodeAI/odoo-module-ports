# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestContractPortalTemplates(HttpCase):
    def test_contract_page_content(self):
        partner = self.env["res.partner"].create({"name": "Portal Test Partner"})
        contract = self.env["contract.contract"].create(
            {"name": "Portal Test Contract", "partner_id": partner.id}
        )
        contract.message_subscribe(partner_ids=self.env.user.partner_id.ids)
        self.authenticate("admin", "admin")
        response = self.url_open("/my/contracts/%s" % contract.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="card_header"', response.content)
        self.assertIn(b'id="card_body"', response.content)
        self.assertIn(b'Portal Test Partner', response.content)
