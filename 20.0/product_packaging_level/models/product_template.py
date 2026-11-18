# Copyright 2019-2020 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    packaging_ids = fields.Many2many(
        "uom.uom", related="uom_ids", string="Product Packagings", readonly=True
    )

    @api.constrains("uom_ids")
    def _check_one_packaging_level_per_product(self):
        for product in self:
            levels = [
                packaging.packaging_level_id.id
                for packaging in product.uom_ids
                if not packaging.packaging_level_id.is_default
                and packaging.packaging_level_id.name_policy == "by_package_level"
            ]
            if len(set(levels)) != len(levels):
                raise ValidationError(
                    self.env._(
                        "It is forbidden to have different packagings "
                        "with the same level for a given product ({})."
                    ).format(product.display_name)
                )

    def write(self, vals):
        res = super().write(vals)
        if "uom_ids" in vals:
            self._check_one_packaging_level_per_product()
        return res
