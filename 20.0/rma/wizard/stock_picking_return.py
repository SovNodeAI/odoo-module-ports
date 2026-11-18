# Copyright 2020 Tecnativa - Ernesto Tejeda
# Copyright 2023 Michael Tietz (MT Software) <mtietz@mt-software.de>
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from copy import deepcopy

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    rma_operation_id = fields.Many2one(
        comodel_name="rma.operation",
        string="Operation",
        compute="_compute_rma_operation_id",
        store=True,
        readonly=False,
    )
    return_product_id = fields.Many2one(
        "product.product",
        help="Product to be returned if it's different from the originally delivered "
        "item.",
    )
    different_return_product = fields.Boolean(
        related="rma_operation_id.different_return_product"
    )

    @api.depends("picking_id.rma_operation_id")
    def _compute_rma_operation_id(self):
        for rec in self:
            if rec.picking_id.rma_operation_id:
                rec.rma_operation_id = rec.picking_id.rma_operation_id

    def _prepare_rma_vals(self):
        self.ensure_one()
        origin_move = self.origin_returned_move_id or self
        picking = origin_move.picking_id or self.picking_id
        warehouse = picking.picking_type_id.warehouse_id
        if not warehouse:
            # Dropship compatibility
            warehouse = self.env["stock.warehouse"].search(
                [("company_id", "=", picking.company_id.id)],
                limit=1,
            )
        vals = {
            "move_id": origin_move.id,
            "product_id": origin_move.product_id.id,
            "product_uom_qty": self.product_uom_qty,
            "product_uom": self.uom_id.id,
            "location_id": warehouse.rma_loc_id.id,
            "operation_id": self.rma_operation_id.id,
            "return_product_id": self.return_product_id.id,
        }
        # RMA from RMA compatibility
        rma = origin_move.rma_id
        if rma:
            vals.update(
                partner_id=rma.partner_id.id,
                partner_shipping_id=rma.partner_shipping_id.id,
                partner_invoice_id=rma.partner_invoice_id.id,
            )
        return vals


class StockPicking(models.Model):
    _inherit = "stock.picking"

    create_rma = fields.Boolean(string="Create RMAs")
    rma_operation_id = fields.Many2one(
        comodel_name="rma.operation",
        string="Requested operation",
    )

    @api.onchange("create_rma")
    def _onchange_create_rma(self):
        if self.create_rma:
            # We want to avoid setting the return move `to_refund` as it will change
            # the delivered quantities in the sale and set them to invoice.
            self.move_ids.to_refund = False

    def _prepare_rma_partner_values(self):
        self.ensure_one()
        partner = self.partner_id
        partner_address = partner.address_get(["invoice", "delivery"])
        partner_invoice_id = partner_address.get("invoice", False)
        partner_shipping_id = partner_address.get("delivery", False)
        return (
            partner,
            partner_invoice_id and partner.browse(partner_invoice_id) or partner,
            partner_shipping_id and partner.browse(partner_shipping_id) or partner,
        )

    def _prepare_rma_vals(self):
        partner, partner_invoice, partner_shipping = self._prepare_rma_partner_values()
        origin = self.return_id.name
        return {
            "user_id": self.env.user.id,
            "partner_id": partner.id,
            "partner_shipping_id": partner_shipping.id,
            "partner_invoice_id": partner_invoice.id,
            "origin": origin,
            "picking_id": self.return_id.id,
            "company_id": self.company_id.id,
        }

    def _prepare_rma_vals_list(self):
        vals_list = []
        for return_picking in self:
            global_vals = return_picking._prepare_rma_vals()
            for line in return_picking.move_ids:
                if not line.origin_returned_move_id or line.uom_id.is_zero(
                    line.product_uom_qty
                ):
                    continue
                vals = deepcopy(global_vals)
                vals.update(line._prepare_rma_vals())
                vals_list.append(vals)
        return vals_list

    def button_validate(self):
        """Create one or more 'confirmed' RMAs instead of validating the return
        picking when 'Create RMAs' checkbox is checked in the return picking.
        New RMAs will be linked to the delivery picking as the origin delivery
        and also RMAs will be linked to the returned picking as the 'Receipt'.
        """
        if self.return_id and self.create_rma:
            return self.action_create_returns()
        return super().button_validate()

    def action_create_returns(self):
        """Create one or more 'confirmed' RMAs after returning a delivery picking
        in case 'Create RMAs' checkbox is checked in the return picking.
        """
        self.ensure_one()
        if not self.create_rma:
            return {
                "name": self.env._("Returned Picking"),
                "view_mode": "form",
                "res_model": "stock.picking",
                "res_id": self.id,
                "type": "ir.actions.act_window",
            }
        if not self.partner_id:
            raise ValidationError(
                self.env._(
                    "You must specify the 'Customer' in the "
                    "'Stock Picking' from which RMAs will be created"
                )
            )
        vals_list = self._prepare_rma_vals_list()
        rmas = self.env["rma"].create(vals_list)
        rmas.action_confirm()
        picking = rmas.reception_move_id.picking_id
        picking = picking and picking[0] or picking
        ctx = dict(self.env.context)
        ctx.update(
            {
                "default_partner_id": picking.partner_id.id,
                "search_default_picking_type_id": picking.picking_type_id.id,
                "search_default_draft": False,
                "search_default_assigned": False,
                "search_default_confirmed": False,
                "search_default_ready": False,
                "search_default_planning_issues": False,
                "search_default_available": False,
            }
        )
        # The RMAs receptions replace the draft return picking
        self.unlink()
        return {
            "name": self.env._("Returned Picking"),
            "view_mode": "form,list,calendar",
            "res_model": "stock.picking",
            "res_id": picking.id,
            "type": "ir.actions.act_window",
            "context": ctx,
        }
