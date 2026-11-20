# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    # Odoo 20 removed the currency_id field of res.partner.bank (it was a
    # plain, usually empty, field in Odoo 19). It is still read by
    # account_payment_sepa_base when it generates the debtor account block of
    # the pain file, so we keep the same field available.
    currency_id = fields.Many2one("res.currency", string="Currency")
