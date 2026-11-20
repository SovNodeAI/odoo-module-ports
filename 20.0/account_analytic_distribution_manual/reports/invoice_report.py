# Copyright 2024 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    manual_distribution_id = fields.Many2one("account.analytic.distribution.manual")

    def _select_list(self, table):
        return super()._select_list(table) + [table.manual_distribution_id]
