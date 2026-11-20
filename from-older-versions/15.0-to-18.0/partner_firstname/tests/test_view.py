# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Check the partner form the way the web client reads it.

The web client OR-merges the ``required`` modifier of every occurrence of a
field and validates required fields even when they are readonly. A ``name``
field that is readonly for individuals must therefore not be required for
them, or a contact typed through firstname/lastname cannot be saved.
"""

from lxml import etree

from odoo.tests import TransactionCase
from odoo.tools.safe_eval import safe_eval


class PartnerFormViewCase(TransactionCase):
    def _individual_required(self, view_xmlid):
        arch = self.env["res.partner"].get_view(
            self.env.ref(view_xmlid).id, "form"
        )["arch"]
        node = etree.fromstring(arch).xpath("//field[@id='individual']")[0]
        return node.get("required")

    def test_individual_name_not_required_for_contacts(self):
        for view_xmlid in (
            "base.view_partner_simple_form",
            "base.view_partner_form",
        ):
            required = self._individual_required(view_xmlid)
            self.assertFalse(
                safe_eval(required, {"is_company": False, "type": "contact"}),
                "The individual name is required although it is readonly",
            )
            self.assertTrue(
                safe_eval(required, {"is_company": True, "type": "contact"}),
                "The company name must stay required",
            )
