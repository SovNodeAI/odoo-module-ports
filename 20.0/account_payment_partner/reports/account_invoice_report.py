# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    payment_mode_id = fields.Many2one(
        comodel_name="account.payment.mode",
        string="Payment mode",
        readonly=True,
    )

    # No _select_list() here. This module comes from the 18.0 branch; since 19.0 the
    # module it depends on, account_payment_mode, carries the same field and adds the
    # column to the report itself. Adding it a second time makes the column ambiguous
    # and the invoice analysis fails.
