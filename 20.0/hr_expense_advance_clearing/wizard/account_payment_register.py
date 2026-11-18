# Copyright 2020 Ecosoft Co., Ltd (https://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)


from odoo import _, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _finalize_clearing_payments(self, payments):
        """Mark confirmed clearing payments as paid and preserve drafts."""
        for payment in payments.filtered(lambda payment: payment.state == "paid"):
            payment.write({"move_id": payment.move_id.id, "state": "paid"})

    def _validate_return_advance_source(self):
        if self.env.context.get("hr_return_advance") and not any(
            self.env.context.get("active_ids", [])
        ):
            raise UserError(
                _("You can only return an advance from its journal entry.")
            )

    def _validate_over_return(self):
        """Actual remaining = amount to clear - clear pending
        and it is not legit to return more than remaining"""
        clearings = (
            self.env["hr.expense"]
            .browse(self.env.context.get("clearing_sheet_ids", []))
            .filtered(lambda expense: expense.state == "approved")
        )
        amount_not_clear = sum(clearings.mapped("total_amount"))
        actual_remaining = self.source_amount_currency - amount_not_clear
        more_info = ""
        symbol = self.source_currency_id.symbol
        if amount_not_clear:
            more_info = _("\nNote: pending amount clearing is %(symbol)s%(amount)s") % {
                "symbol": symbol,
                "amount": f"{amount_not_clear:,.2f}",
            }
        if float_compare(self.amount, actual_remaining, 2) == 1:
            raise UserError(
                _(
                    "You cannot return advance more than actual remaining "
                    "(%(symbol)s%(amount)s)%(more_info)s"
                )
                % {
                    "symbol": symbol,
                    "amount": f"{actual_remaining:,.2f}",
                    "more_info": more_info,
                }
            )

    def _init_payments(self, to_process, edit_mode=False):
        if self.env.context.get("hr_return_advance"):
            self._validate_over_return()
            active_ids = self.env.context.get("active_ids", [])
            if self.env.context.get("active_model") == "account.move":
                lines = self.env["account.move"].browse(active_ids).line_ids
            elif self.env.context.get("active_model") == "account.move.line":
                lines = self.env["account.move.line"].browse(active_ids)

            if self.env.context.get("active_model") == "account.move":
                expense = self.env["account.move"].browse(active_ids).expense_ids
            else:
                expense = lines.expense_id
            for x in to_process:
                x["create_vals"]["partner_type"] = "customer"
                x["create_vals"]["advance_id"] = expense.id

        payments = super()._init_payments(to_process, edit_mode)
        return payments

    def default_get(self, fields_list):
        self._validate_return_advance_source()
        return super().default_get(fields_list)

    def action_create_payments(self):
        self._validate_return_advance_source()
        return super().action_create_payments()

    def _create_payments(self):
        """Update the payment state when the clearing amount exceeds the advance."""
        self._validate_return_advance_source()
        payments = super()._create_payments()
        if self.env.context.get("expense_clearing"):
            self._finalize_clearing_payments(payments)
        return payments
