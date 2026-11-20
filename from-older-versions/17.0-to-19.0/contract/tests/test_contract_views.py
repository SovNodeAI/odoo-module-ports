# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.tests import common


class TestContractViews(common.TransactionCase):
    def test_contract_form_chatter(self):
        arch = self.env["contract.contract"].get_view(
            view_id=self.env.ref("contract.contract_contract_form_view").id,
            view_type="form",
        )["arch"]
        root = etree.fromstring(arch)
        self.assertIsNotNone(root.find("chatter"))
        self.assertFalse(root.xpath(".//div[@class='oe_chatter']"))
        self.assertFalse(
            root.xpath(
                ".//field[@widget='mail_followers' or @widget='mail_activity'"
                " or @widget='mail_thread']"
            )
        )

    def test_contract_line_search_unsupported_operator(self):
        self.assertIs(
            self.env["contract.line"]._search_state("ilike", "upcoming"),
            NotImplemented,
        )
