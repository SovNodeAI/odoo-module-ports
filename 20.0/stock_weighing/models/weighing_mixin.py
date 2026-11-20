# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.fields import Domain


class WeightMixin(models.AbstractModel):
    _name = "weighing.mixin"
    _description = "To be used by stock.move and stock.move.line"

    has_weight = fields.Boolean(
        compute="_compute_has_weight", search="_search_has_weight"
    )

    @api.model
    def _has_weigh_domain(self):
        """Plug in to change behavior"""
        return [
            (
                "uom_id",
                "child_of",
                self.env.ref("uom.product_uom_gram").id,
            ),
        ]

    @api.depends("uom_id")
    def _compute_has_weight(self):
        """Product UOM is a weighed one"""
        self.env.ref("uom.product_uom_gram")
        self.has_weight = False
        self.filtered_domain(self._has_weigh_domain()).has_weight = True

    def _search_has_weight(self, operator, value):
        # Odoo 19 and 20 call this with 'in' / 'not in' and a set of values:
        # ('has_weight', '=', True) arrives as ('has_weight', 'in', {True})
        # (odoo/orm/domains.py, _operator_equal_as_in). Any other operator is
        # left to Odoo's own fallback.
        if operator not in ("in", "not in"):
            return NotImplemented
        domain = Domain(
            "uom_id", "child_of", self.env.ref("uom.product_uom_gram").id
        )
        values = {bool(v) for v in value}
        if values == {True}:
            result = domain
        elif values == {False}:
            result = ~domain
        else:
            result = Domain.TRUE if values else Domain.FALSE
        return result if operator == "in" else ~result
