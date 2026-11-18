# Copyright 2019 Kitti Upariphutthiphong <kittiu@ecosoft.co.th>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ast

from odoo import Command, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero


class HrExpenseAdvanceClearing(models.Model):
    _inherit = "hr.expense"

    advance_sheet_id = fields.Many2one(
        comodel_name="hr.expense",
        string="Clear Advance",
        domain="[('advance', '=', True), ('employee_id', '=', employee_id),"
        " ('clearing_residual', '>', 0.0)]",
        help="Show remaining advance of this employee",
    )
    clearing_sheet_ids = fields.One2many(
        comodel_name="hr.expense",
        inverse_name="advance_sheet_id",
        string="Clearing Sheet",
        readonly=True,
        help="Show reference clearing on advance",
    )
    clearing_count = fields.Integer(
        compute="_compute_clearing_count",
    )
    payment_return_ids = fields.One2many(
        comodel_name="account.payment",
        inverse_name="advance_id",
        string="Payment Return",
        readonly=True,
        help="Show reference return advance on advance",
    )
    return_count = fields.Integer(compute="_compute_return_count", compute_sudo=True)
    clearing_residual = fields.Monetary(
        string="Amount to clear",
        compute="_compute_clearing_residual",
        store=True,
        help="Amount to clear of this expense in company currency",
    )
    advance_sheet_residual = fields.Monetary(
        string="Advance Remaining",
        related="advance_sheet_id.clearing_residual",
        store=True,
        help="Remaining amount to clear the selected advance",
    )
    amount_payable = fields.Monetary(
        string="Payable Amount",
        compute="_compute_amount_payable",
        help="Final register payment amount even after advance clearing",
    )
    clearing_journal_id = fields.Many2one(
        comodel_name="account.journal",
        check_company=True,
        domain="[('type', '=', 'general')]",
        compute="_compute_clearing_journal_id",
        store=True,
        readonly=False,
        help="Miscellaneous journal used to post the clearing journal entry.",
    )

    @api.depends("company_id", "advance_sheet_id")
    def _compute_clearing_journal_id(self):
        for expense in self:
            expense.clearing_journal_id = expense.company_id.clearing_journal_id

    @api.constrains("advance_sheet_id", "advance")
    def _check_advance_expense(self):
        if self.filtered(lambda expense: expense.advance and expense.advance_sheet_id):
            raise ValidationError(
                self.env._(
                    "An advance expense cannot also be used to clear an advance"
                )
            )

    @api.depends(
        "account_move_id.state",
        "account_move_id.payment_state",
        "account_move_id.origin_payment_id.state",
        "approval_state",
        "amount_residual",
    )
    def _compute_state(self):
        """Fully cleared expenses are paid although their entry has no payable line."""
        super()._compute_state()
        for expense in self:
            if (
                expense.advance_sheet_id
                and expense.account_move_id.state == "posted"
                and not expense.account_move_id.amount_residual
            ):
                expense.state = "paid"

    def _get_product_advance(self):
        return self.env.ref("hr_expense_advance_clearing.product_emp_advance", False)

    @api.depends("account_move_id.line_ids.amount_residual")
    def _compute_clearing_residual(self):
        for expense in self:
            emp_advance = expense._get_product_advance()
            residual_company = 0.0
            if emp_advance:
                property_account_expense_id = emp_advance.with_company(
                    expense.company_id
                ).property_account_expense_id
                for line in expense.sudo().account_move_id.line_ids:
                    if line.account_id == property_account_expense_id:
                        residual_company += line.amount_residual
            expense.clearing_residual = residual_company

    @api.depends("account_move_id.line_ids.amount_residual")
    def _compute_amount_payable(self):
        for expense in self:
            rec_lines = expense.account_move_id.line_ids.filtered(
                lambda line: line.credit
                and line.account_id.reconcile
                and not line.reconciled
            )
            expense.amount_payable = -sum(rec_lines.mapped("amount_residual"))

    @api.depends("clearing_sheet_ids")
    def _compute_clearing_count(self):
        for expense in self:
            expense.clearing_count = len(expense.clearing_sheet_ids)

    @api.depends("payment_return_ids")
    def _compute_return_count(self):
        for expense in self:
            expense.return_count = len(expense.payment_return_ids)

    def _get_move_line_vals(self):
        self.ensure_one()
        move_line_vals = []
        advance_to_clear = self.advance_sheet_residual
        emp_advance = self._get_product_advance()
        account_advance = emp_advance.with_company(
            self.company_id
        ).property_account_expense_id
        for expense in self:
            move_line_name = (
                f"{expense.employee_id.name}: {expense.name.splitlines()[0][:64]}"
            )
            partner_id = expense.employee_id.sudo().work_contact_id.id

            total_amount = -expense.total_amount
            total_amount_currency = -expense.total_amount_currency

            move_line_src = expense._get_move_line_src(move_line_name, partner_id)
            move_line_values = [move_line_src]
            move_line_dst = expense._get_move_line_dst(
                move_line_name,
                partner_id,
                total_amount,
                total_amount_currency,
                account_advance,
            )

            credit = move_line_dst["credit"]
            remain_payable = 0.0
            payable_move_line = []
            rounding = expense.currency_id.rounding
            if float_compare(
                credit, advance_to_clear, precision_rounding=rounding
            ) == 1:
                remain_payable = credit - advance_to_clear
                move_line_dst.update(
                    {"credit": advance_to_clear, "amount_currency": -advance_to_clear}
                )
                advance_to_clear = 0.0
                account_dest = expense._get_expense_account_destination()
                payable_move_line = move_line_dst.copy()
                payable_move_line.update(
                    {
                        "credit": remain_payable,
                        "amount_currency": -remain_payable,
                        "account_id": account_dest,
                    }
                )
            else:
                advance_to_clear -= credit

            if not float_is_zero(move_line_dst["credit"], precision_rounding=rounding):
                move_line_values.append(move_line_dst)
            if payable_move_line:
                move_line_values.append(payable_move_line)
            move_line_vals.extend(move_line_values)
        return move_line_vals

    def _prepare_receipts_vals(self):
        """Create a clearing entry instead of an employee receipt."""
        clearing_expenses = self.filtered(
            lambda expense: expense.advance_sheet_id
            and expense.payment_mode == "own_account"
        )
        return_vals = super(
            HrExpenseAdvanceClearing, self - clearing_expenses
        )._prepare_receipts_vals()
        for expense in clearing_expenses:
            if expense.advance_sheet_residual <= 0.0:
                raise ValidationError(
                    self.env._(
                        "Advance: %(name)s has no amount to clear", name=expense.name
                    )
                )
            vals = super(HrExpenseAdvanceClearing, expense)._prepare_receipts_vals()[0]
            vals.update(
                {
                    "move_type": "entry",
                    "journal_id": expense.clearing_journal_id.id,
                    "line_ids": [
                        Command.create(line)
                        for line in expense._get_move_line_vals()
                    ],
                }
            )
            return_vals.append(vals)
        return return_vals

    def _check_can_approve(self):
        """Check advance residual before approval."""
        for expense in self.filtered("advance_sheet_id"):
            if expense.advance_sheet_residual <= 0.0:
                raise ValidationError(
                    self.env._(
                        "Advance: %(name)s has no amount to clear",
                        name=expense.advance_sheet_id.name,
                    )
                )
        return super()._check_can_approve()

    def open_clear_advance(self):
        self.ensure_one()
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "hr_expense_advance_clearing.action_hr_expense_sheet_advance_clearing"
        )
        context = ast.literal_eval(result["context"])
        context.update(
            {
                "default_advance_sheet_id": self.id,
                "default_employee_id": self.employee_id.id,
            }
        )
        result["context"] = context
        return result

    def get_domain_advance_sheet_expense_line(self):
        return self.advance_sheet_id.filtered("clearing_product_id")

    def create_clearing_expense_line(self, line):
        clear_advance = self._prepare_clear_advance(line)
        return self.env["hr.expense"].new(clear_advance)

    @api.onchange("advance_sheet_id")
    def _onchange_advance_sheet_id(self):
        if not self.advance_sheet_id:
            if self.av_line_id:
                self.av_line_id = False
            return

        self.advance_sheet_id.sudo().read(["id"])
        line = self.get_domain_advance_sheet_expense_line()[:1]
        if line:
            self.update(self._prepare_clear_advance(line))

    def _prepare_clear_advance(self, line):
        clear_line_dict = {
            "advance": False,
            "advance_sheet_id": self.advance_sheet_id.id,
            "name": line.clearing_product_id.display_name,
            "product_id": line.clearing_product_id.id,
            "clearing_product_id": False,
            "date": fields.Date.context_today(self),
            "account_id": False,
            "product_uom_id": False,
            "av_line_id": line.id,
        }
        clear_line = self.env["hr.expense"].new(clear_line_dict)
        clear_line._compute_account_id()

        adv_dict = line._convert_to_write(line._cache)
        del_cols = set.union(
            {key for key, value in line._fields.items() if value.type == "one2many"},
            self.env["mail.thread"]._fields.keys(),
            self.env["mail.activity.mixin"]._fields.keys(),
            {
                key
                for key, value in line._fields.items()
                if value.readonly
            },
            clear_line_dict.keys(),
        )
        adv_dict = {key: value for key, value in adv_dict.items() if key not in del_cols}
        clear_line.update(adv_dict)
        clearing_dict = clear_line._convert_to_write(clear_line._cache)
        return {
            key: isinstance(value, list)
            and all(isinstance(item, int) for item in value)
            and [(Command.SET, 0, value)]
            or value
            for key, value in clearing_dict.items()
        }

    def action_open_clearings(self):
        self.ensure_one()
        return {
            "name": self.env._("Clearing Sheets"),
            "type": "ir.actions.act_window",
            "res_model": "hr.expense",
            "view_mode": "list,form",
            "domain": [("id", "in", self.clearing_sheet_ids.ids)],
        }

    def action_open_payment_return(self):
        self.ensure_one()
        return {
            "name": self.env._("Payment Return"),
            "type": "ir.actions.act_window",
            "res_model": "account.payment",
            "view_mode": "list,form",
            "domain": [("id", "in", self.payment_return_ids.ids)],
        }

    def action_register_payment(self):
        self.ensure_one()
        action = self.account_move_id.with_context(
            hr_return_advance=self.env.context.get("hr_return_advance", False)
        ).action_register_payment()
        if self.env.context.get("hr_return_advance"):
            action["context"].update(
                {
                    "clearing_sheet_ids": self.clearing_sheet_ids.ids,
                }
            )
        return action
