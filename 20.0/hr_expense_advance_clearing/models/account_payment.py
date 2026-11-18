# Copyright 2022 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    advance_id = fields.Many2one(
        comodel_name="hr.expense",
        readonly=True,
    )

    def _synchronize_to_moves(self, changed_fields):
        """Keep return-advance payment lines instead of rebuilding them."""
        if self.filtered("advance_id"):
            return
        return super()._synchronize_to_moves(changed_fields)

    def _get_clearing_moves(self):
        self.ensure_one()
        return self.invoice_ids.filtered(
            lambda move: move.state == "posted"
            and move.move_type == "entry"
            and move.expense_ids.advance_sheet_id
        )

    def action_draft(self):
        # Odoo 20 no longer unreconciles when resetting a payment to draft.
        # Keep the clearing link so that the payment can reconcile again on posting.
        clearing_moves = {payment: payment._get_clearing_moves() for payment in self}
        for payment, moves in clearing_moves.items():
            if moves:
                (moves + payment.move_id).line_ids.remove_move_reconcile()
        res = super().action_draft()
        for payment, moves in clearing_moves.items():
            payment.invoice_ids |= moves
        return res

    def action_post(self):
        res = super().action_post()
        for payment in self.filtered("move_id"):
            clearing_moves = payment._get_clearing_moves()
            if not clearing_moves:
                continue

            lines = (clearing_moves + payment.move_id).line_ids.filtered(
                lambda line: line.account_id.reconcile
                and not line.reconciled
                and line.account_id.account_type
                in ("asset_receivable", "liability_payable")
            )
            for account in lines.account_id:
                account_lines = lines.filtered_domain([("account_id", "=", account.id)])
                if len(account_lines) > 1:
                    account_lines.reconcile()
        return res

    @api.model
    def _get_valid_payment_account_types(self):
        account_types = super()._get_valid_payment_account_types()
        if self.env.context.get("hr_return_advance"):
            account_types.append("asset_current")
        return account_types
