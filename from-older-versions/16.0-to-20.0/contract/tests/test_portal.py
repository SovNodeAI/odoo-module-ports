# Copyright 2020 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import odoo.tests
from odoo import http
from odoo.tests import new_test_user


@odoo.tests.tagged("post_install", "-at_install")
class TestContractPortal(odoo.tests.HttpCase):
    def test_tour(self):
        partner = self.env["res.partner"].create({"name": "partner test contract"})
        contract = self.env["contract.contract"].create(
            {"name": "Test Contract", "partner_id": partner.id}
        )
        user_portal = new_test_user(
            self.env,
            login="portal",
            password="portal",
            groups="base.group_portal",
            partner_id=partner.id,
        )
        contract.message_subscribe(partner_ids=user_portal.partner_id.ids)
        self.start_tour("/my", "contract_portal_tour", login="portal")
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
