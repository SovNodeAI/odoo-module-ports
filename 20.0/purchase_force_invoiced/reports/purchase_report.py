# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
# Copyright 2022 Tecnativa - Pedro M. Baeza
from odoo import models
from odoo.tools import SQL


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    def _select_list(self, table):
        """Put quantity to be billed as 0 if it has been forced."""
        select_list = super()._select_list(table)
        uom_ratio = SQL(
            "(COALESCE(%s, 1) / NULLIF(COALESCE(%s, 1), 0.0))",
            table.uom_id.factor,
            table.product_id.uom_id.factor,
        )
        select_list[-1] = SQL(
            """CASE WHEN %(force_invoiced)s THEN 0.0
                   WHEN %(purchase_method)s = 'purchase'
                   THEN SUM(%(qty)s * %(uom_ratio)s) - SUM(%(invoiced)s * %(uom_ratio)s)
                   ELSE SUM(%(received)s * %(uom_ratio)s) - SUM(%(invoiced)s * %(uom_ratio)s)
                  END AS qty_to_be_billed""",
            force_invoiced=table.order_id.force_invoiced,
            purchase_method=table.product_id.product_tmpl_id.purchase_method,
            qty=table.product_qty,
            invoiced=table.qty_invoiced,
            received=table.qty_received,
            uom_ratio=uom_ratio,
        )
        return select_list
