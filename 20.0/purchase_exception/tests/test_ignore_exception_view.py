# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestIgnoreExceptionIsShown(TransactionCase):
    def test_checkbox_is_not_inside_a_hidden_container(self):
        """On a confirmed order the "Ignore Exceptions" checkbox can be seen.

        Its own rule shows it when the order is confirmed; no container around
        it may hide it under another condition.
        """
        # the checkbox is for exception managers only
        manager = self.env.ref("base.user_admin")
        manager.group_ids |= self.env.ref(
            "base_exception.group_exception_rule_manager"
        )
        view = self.env.ref("purchase.purchase_order_form")
        arch = etree.fromstring(
            self.env["purchase.order"]
            .with_user(manager)
            .get_view(view.id, "form")["arch"]
        )
        nodes = arch.xpath("//field[@name='ignore_exception']")
        self.assertTrue(nodes)
        shown = [
            node
            for node in nodes
            if not any(parent.get("invisible") for parent in node.iterancestors())
        ]
        self.assertTrue(shown, "every ignore_exception field sits in a hidden container")
        self.assertEqual(shown[0].get("invisible"), "state != 'purchase'")
