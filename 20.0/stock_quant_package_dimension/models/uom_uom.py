# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class UomUom(models.Model):
    # In Odoo 20 a product packaging is a UoM available on the product
    # (see stock_quant_package_product_packaging), so the dimensions a
    # package is filled with are the dimensions of that UoM. They were
    # carried by product.packaging in previous versions.
    _inherit = "uom.uom"

    packaging_length = fields.Integer(string="Length")
    width = fields.Integer()
    height = fields.Integer()
    weight = fields.Float()

    # Same as product.uom (product_packaging_dimension)
    length_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensions Units of Measure",
        help="UoM for packaging length, height, width (based on lenght UoM)",
        default=lambda self: self.env[
            "product.template"
        ]._get_length_uom_id_from_ir_config_parameter(),
    )
    weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Weight Units of Measure",
        help="Weight Unit of Measure",
        default=lambda self: self.env[
            "product.template"
        ]._get_weight_uom_id_from_ir_config_parameter(),
    )
    volume_uom_id = fields.Many2one(
        "uom.uom",
        string="Volume Units of Measure",
        help="Packaging volume unit of measure",
        default=lambda self: self.env[
            "product.template"
        ]._get_volume_uom_id_from_ir_config_parameter(),
    )
