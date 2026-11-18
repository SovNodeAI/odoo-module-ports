# © 2017 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError

from odoo.addons.base.tests.common import BaseCommon


class TestBank(BaseCommon):
    _test_user_groups = None

    def test_bank(self):
        bank = self.env["res.partner.bank"].search([], limit=1)
        if not bank:
            # This should only happen if we don't have demo data
            bank = self.env["res.partner.bank"].create(
                {
                    "account_number": "FIDCFR21XXX",
                    "bank_bic": "FIDCFR21XXX",
                    "partner_id": self.env["res.partner"]
                    .create({"name": "Fiducial Banque"})
                    .id,
                    "street": "38 rue Sergent Michel Berthet",
                    "zip": "69009",
                    "city": "Lyon",
                    "country_id": self.env.ref("base.fr").id,
                }
            )
        with self.assertRaises(ValidationError):
            bank.bank_bic = "TEST"
