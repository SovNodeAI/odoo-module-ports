from odoo import fields, models, tools


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    @property
    def _table_sql(self):
        today = fields.Date.context_today(self)
        self.env["account.move.line"].check_access("read")
        query = self.env["account.move.line"].sudo().with_context(date_to=today)._search(
            [
                ("move_type", "in", self._fields["move_type"].get_values(self.env)),
                ("account_id", "!=", False),
                "|",
                ("display_type", "=", "product"),
                ("invoice_global_discount_id", "!=", False),
            ]
        )
        query.add_where(
            tools.SQL(
                "%s = %s", query.table._sudo().move_id.company_id, query.table.company_id
            )
        )
        return query.subselect(*self._select_list(query.table))
