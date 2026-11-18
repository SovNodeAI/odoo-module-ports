# Copyright 2021 Ecosoft Co., Ltd. (http://www.ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    advance_sheet_ids = fields.One2many(
        comodel_name="hr.expense",
        inverse_name="employee_id",
        domain=[("advance", "=", True)],
        readonly=True,
    )
    advance_count = fields.Integer(
        string="# of Advance",
        compute="_compute_advance_count",
        help="Count advances for this employee",
    )

    @api.depends("advance_sheet_ids")
    def _compute_advance_count(self):
        for employee in self:
            employee.advance_count = len(employee.advance_sheet_ids)

    def action_open_advance_clearing(self):
        self.ensure_one()
        return {
            "name": self.env._("Advance Sheet"),
            "type": "ir.actions.act_window",
            "res_model": "hr.expense",
            "view_mode": "list,form",
            "domain": [("id", "in", self.advance_sheet_ids.ids)],
        }


class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    advance_sheet_ids = fields.Many2many(
        comodel_name="hr.expense",
        compute="_compute_advance_sheet_ids",
    )
    advance_count = fields.Integer(related="employee_id.advance_count")

    @api.depends("employee_id")
    def _compute_advance_sheet_ids(self):
        advances = self.env["hr.expense"].search(
            [("employee_id", "in", self.ids), ("advance", "=", True)]
        )
        for employee in self:
            employee.advance_sheet_ids = advances.filtered(
                lambda expense: expense.employee_id.id == employee.id
            )

    def action_open_advance_clearing(self):
        self.ensure_one()
        return self.employee_id.action_open_advance_clearing()
