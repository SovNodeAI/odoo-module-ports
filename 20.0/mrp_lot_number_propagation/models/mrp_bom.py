# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    lot_number_propagation = fields.Boolean(
        default=False,
        help=(
            "Allow to propagate the lot/serial number "
            "from a component to the finished product."
        ),
    )
    display_lot_number_propagation = fields.Boolean(
        compute="_compute_display_lot_number_propagation"
    )

    @api.depends(
        "type",
        "product_tmpl_id.tracking",
        "product_qty",
        "uom_id",
        "bom_line_ids.product_id.tracking",
        "bom_line_ids.product_qty",
        "bom_line_ids.uom_id",
    )
    def _compute_display_lot_number_propagation(self):
        """Check if a lot number can be propagated.

        A lot number can be propagated from a component to the finished product if:
        - the type of the BoM is normal (Manufacture this product)
        - the finished product is tracked by serial number
        - the quantity of the finished product is 1 and its UoM is unit
        - there is at least one bom line, with a component tracked by serial,
          having a quantity of 1 and its UoM is unit
        """
        uom_unit = self.env.ref("uom.product_uom_unit")
        for bom in self:
            bom.display_lot_number_propagation = (
                bom.type in self._get_lot_number_propagation_bom_types()
                and bom.product_tmpl_id.tracking == "serial"
                and bom.uom_id.compare(bom.product_qty, 1) == 0
                and bom.uom_id == uom_unit
                and bom._has_tracked_product_to_propagate()
            )

    def _get_lot_number_propagation_bom_types(self):
        return ["normal"]

    def _has_tracked_product_to_propagate(self):
        self.ensure_one()
        uom_unit = self.env.ref("uom.product_uom_unit")
        for line in self.bom_line_ids:
            if (
                line.product_id.tracking == "serial"
                and line.uom_id.compare(line.product_qty, 1) == 0
                and line.uom_id == uom_unit
            ):
                return True
        return False

    @api.onchange("display_lot_number_propagation")
    def onchange_display_lot_number_propagation(self):
        if not self.display_lot_number_propagation:
            self.lot_number_propagation = False

    @api.constrains("lot_number_propagation")
    def _check_propagate_lot_number(self):
        for bom in self:
            if not bom.lot_number_propagation:
                continue
            if not bom.bom_line_ids.filtered("propagate_lot_number"):
                raise ValidationError(
                    self.env._(
                        "With 'Lot Number Propagation' enabled, a line has "
                        "to be configured with the 'Propagate Lot Number' option."
                    )
                )
