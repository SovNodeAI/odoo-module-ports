# Copyright 2020 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    # Odoo 20 removed ``account.journal.bank_id``: the bank is now reached
    # through the journal's bank account (``bank_account_id``).
    bank_id = fields.Many2one(
        comodel_name="res.bank",
        related="bank_account_id.bank_id",
    )

    bank_code_bc = fields.Char(related="bank_id.code_bc")
