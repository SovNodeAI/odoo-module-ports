# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models, tools


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_product_packagings(self):
        """Return the packagings of the product.

        In Odoo 20 a packaging is a UoM available on the product.
        """
        self.ensure_one()
        return self.uom_ids | self.extra_uom_ids

    def _get_packaging_qty(self, packaging):
        """Quantity of the packaging expressed in the main UoM of the product."""
        self.ensure_one()
        return packaging._compute_quantity(1, self.uom_id, round=False)

    def _find_best_packaging(self, quantity):
        self.ensure_one()
        packagings = self._get_product_packagings().sorted(
            key=lambda packaging: (
                -self._get_packaging_qty(packaging),
                packaging.sequence,
            )
        )
        for packaging in packagings:
            packaging_qty = self._get_packaging_qty(packaging)
            if tools.float_compare(packaging_qty, 0.0, precision_digits=3) <= 0:
                continue
            if tools.float_compare(packaging_qty, quantity, precision_digits=3) > 0:
                continue
            nb = quantity / packaging_qty
            if tools.float_is_zero(nb - round(nb), precision_digits=3):
                return packaging
        return self.env["uom.uom"]
