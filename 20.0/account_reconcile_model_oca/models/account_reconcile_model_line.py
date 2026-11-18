# Copyright 2025 Victor M.M. Torres, Tecnativa SL
# Licence LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from odoo import api, fields, models


class AccountReconcileModelLine(models.Model):
    _inherit = "account.reconcile.model.line"

    journal_id = fields.Many2one(
        "account.journal",
        string="Journal",
        ondelete="cascade",
        check_company=True,
        store=True,
        readonly=False,
        compute="_compute_journal_id",
    )
    force_tax_included = fields.Boolean(
        string="Tax Included in Price",
        help="Force the tax to be managed as a price included tax.",
    )
    show_force_tax_included = fields.Boolean(compute="_compute_show_force_tax_included")

    @api.onchange("tax_ids")
    def _onchange_tax_ids(self):
        if len(self.tax_ids) != 1:
            self.force_tax_included = False

    @api.depends("tax_ids")
    def _compute_show_force_tax_included(self):
        for record in self:
            record.show_force_tax_included = len(record.tax_ids) == 1

    @api.depends("model_id.rule_type")
    def _compute_journal_id(self):
        self.journal_id = False

    def _get_write_off_move_line_dict(self, balance, currency):
        self.ensure_one()
        return {
            "name": self.label,
            "balance": balance,
            "debit": balance > 0 and balance or 0,
            "credit": balance < 0 and -balance or 0,
            "account_id": self.account_id.id,
            "currency_id": currency.id,
            "analytic_distribution": self.analytic_distribution,
            "reconcile_model_id": self.model_id.id,
            "journal_id": self.journal_id.id,
            "tax_ids": [],
        }
