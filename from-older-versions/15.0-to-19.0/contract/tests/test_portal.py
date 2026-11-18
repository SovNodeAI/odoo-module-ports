# Copyright 2020 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import odoo.tests
from odoo import http


@odoo.tests.tagged("post_install", "-at_install")
class TestContractPortal(odoo.tests.HttpCase):
    def test_tour(self):
        partner = self.env["res.partner"].create({"name": "partner test contract"})
        contract = self.env["contract.contract"].create(
            {"name": "Test Contract", "partner_id": partner.id}
        )
        # Demo data is not installed on the test database, so create the
        # equivalent portal user that the test relies on.
        user_portal = self.env["res.users"].create(
            {
                "name": "Mr Demo Portal",
                "login": "portal",
                "password": "portal",
                "group_ids": [(6, 0, [self.env.ref("base.group_portal").id])],
            }
        )
        contract.message_subscribe(partner_ids=user_portal.partner_id.ids)
        self.start_tour("/", "contract_portal_tour", login="portal")
        # Contract access
        self.authenticate("portal", "portal")
        http.root.session_store.save(self.session)
        url_contract = "/my/contracts/{}?access_token={}".format(
            contract.id,
            contract.access_token,
        )
        self.assertEqual(self.url_open(url=url_contract).status_code, 200)
        contract.message_unsubscribe(partner_ids=user_portal.partner_id.ids)
        self.assertEqual(self.url_open(url=url_contract).status_code, 200)
