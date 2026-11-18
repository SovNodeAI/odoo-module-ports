# Copyright (C) 2024-Today - Akretion (<http://www.akretion.com>).
# @author Magno Costa <magno.costa@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    # Odoo 20 removed ``res.bank`` and flattened its data into
    # ``res.partner.bank``.  The Brazilian CNAB logic still needs the bank
    # directory relation (COMPE code, short name, ...), so it is restored here.
    bank_id = fields.Many2one(comodel_name="res.bank", string="Bank")

    # Odoo 20 stores the bank name as free text on the account; keep it in sync
    # with the restored Brazilian bank directory.
    bank_name = fields.Char(related="bank_id.name", readonly=False)

    @api.constrains("bra_number")
    def _check_bra_number_cnab(self):
        for bank in self:
            if bank.bank_id.code_bc and bank.bra_number and len(bank.bra_number) > 4:
                raise UserError(self.env._("Bank branch code must be four characters."))
