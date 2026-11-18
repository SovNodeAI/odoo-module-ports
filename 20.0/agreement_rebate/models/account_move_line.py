# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.misc import format_date


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    agreement_rebate_settlement_line_ids = fields.Many2many(
        comodel_name="agreement.rebate.settlement.line",
        relation="agreement_rebate_settlement_line_account_invoice_line_rel",
        column1="invoice_line_id",
        column2="settlement_line_id",
        string="Settlement lines",
    )

    @api.depends("agreement_rebate_settlement_line_ids")
    def _compute_label(self):
        res = super()._compute_label()
        for line in self:
            if not line.label:
                continue
            settlements = line.agreement_rebate_settlement_line_ids.settlement_id
            if len(settlements) == 1:
                date_from = format_date(self.env, settlements.date_from)
                date_to = format_date(self.env, settlements.date_to)
                line.label += " - " + self.env._(
                    "Period: %(date_from)s - %(date_to)s",
                    date_from=date_from,
                    date_to=date_to,
                )
        return res
