# Copyright 2023 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_return_sale_order(self):
        self.ensure_one()
        return self.return_id.sale_id or self.sale_id

    def _prepare_rma_partner_values(self):
        sale_order = self._get_return_sale_order()
        if not sale_order:
            return super()._prepare_rma_partner_values()
        return (
            sale_order.partner_id,
            sale_order.partner_invoice_id,
            sale_order.partner_shipping_id,
        )

    def _prepare_rma_vals(self):
        vals = super()._prepare_rma_vals()
        sale_order = self._get_return_sale_order()
        if sale_order:
            vals["order_id"] = sale_order.id
        return vals
