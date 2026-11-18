# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"


    @api.model
    def _prepare_add_missing_fields(self, values):
        # Providing every core onchange field is intentional: the parent
        # blanket onchange still uses the Odoo <=18 purchase taxes_id field.
        values = values.copy()
        values.setdefault("discount", 0.0)
        return super()._prepare_add_missing_fields(values)
