# Copyright 2019-2020 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from collections import OrderedDict

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UomUom(models.Model):
    _inherit = "uom.uom"

    packaging_level_id = fields.Many2one(
        "product.packaging.level",
        required=True,
        ondelete="restrict",
        default=lambda self: self.default_packaging_level_id(),
    )
    barcode_required_for_gtin = fields.Boolean(
        readonly=True, compute="_compute_barcode_required_for_gtin"
    )
    qty_per_level = fields.Char(
        compute="_compute_qty_per_level", string="Qty per package level"
    )
    name_policy = fields.Selection(related="packaging_level_id.name_policy")
    product_ids = fields.Many2many(
        "product.template", compute="_compute_product_ids", search="_search_product_ids"
    )
    name = fields.Char(compute="_compute_name", store=True, readonly=False)
    sequence = fields.Integer(compute="_compute_sequence", store=True, readonly=False)

    def default_packaging_level_id(self):
        return self.env["product.packaging.level"].search(
            [("is_default", "=", True)], limit=1
        )

    @api.model
    def _init_packaging_level(self):
        default_level = self.default_packaging_level_id()
        if default_level:
            self.search([("packaging_level_id", "=", False)]).write(
                {"packaging_level_id": default_level.id}
            )

    def _compute_product_ids(self):
        for uom in self:
            uom.product_ids = self.env["product.template"].search(
                [("uom_ids", "in", uom.ids)]
            )

    def _search_product_ids(self, operator, value):
        products = self.env["product.template"].search([("id", operator, value)])
        return [("id", "in", products.uom_ids.ids)]

    @api.constrains("packaging_level_id")
    def _check_one_packaging_level_per_product(self):
        packages_name_by_level = self.filtered(
            lambda p: p.name_policy == "by_package_level"
        )
        for packaging in packages_name_by_level:
            for product in packaging.product_ids:
                packaging_level_ids = (
                    packaging._check_one_packaging_level_per_product_filter_ids(product)
                )
                if len(set(packaging_level_ids)) != len(packaging_level_ids):
                    raise ValidationError(
                        self.env._(
                            "It is forbidden to have different packagings "
                            "with the same level for a given product ({})."
                        ).format(product.display_name)
                    )

    def _check_one_packaging_level_per_product_filter_ids(self, product=None):
        product = product or self.product_ids[:1]
        return [
            packaging.packaging_level_id.id
            for packaging in product.uom_ids
            if not packaging.packaging_level_id.is_default
        ]

    @api.depends("packaging_level_id")
    def _compute_sequence(self):
        for packaging in self:
            packaging.sequence = packaging.packaging_level_id.sequence

    @api.depends("packaging_level_id", "packaging_level_id.has_gtin", "relative_factor")
    def _compute_barcode_required_for_gtin(self):
        for packaging in self:
            packaging.barcode_required_for_gtin = packaging.packaging_level_id.has_gtin
            if not packaging.relative_factor:
                packaging.barcode_required_for_gtin = False

    @api.depends(
        "product_ids",
        "packaging_level_id",
        "packaging_level_id.code",
        "relative_factor",
        "relative_uom_id",
    )
    def _compute_qty_per_level(self):
        for packaging in self:
            mapping = packaging._get_qty_per_level_mapping()
            packaging.qty_per_level = packaging._format_qty_per_level(mapping)

    def _get_qty_per_level_mapping(self):
        """Retrieve qty for each packaging level.

        :return: mapping {level.code: qty}
        """
        products = self.env["product.template"].search([("uom_ids", "in", self.ids)])
        if not products:
            return self._get_qty_per_level_mapping_from_hierarchy()
        smaller_product_packagings = products.uom_ids.filtered(
            lambda p: p.id != self.id
            and not p.packaging_level_id.is_default
            and self.relative_factor > p.relative_factor > 0.0
        )
        res = OrderedDict()
        for p_pack in smaller_product_packagings.sorted(lambda p: p.relative_factor):
            res[p_pack.packaging_level_id.code] = p_pack.relative_factor
        return res

    def _get_qty_per_level_mapping_from_hierarchy(self):
        res = OrderedDict()
        qty = self.relative_factor
        for packaging in self.relative_uom_id.filtered(
            lambda p: not p.packaging_level_id.is_default
        ):
            if qty > packaging.relative_factor > 0.0:
                res[packaging.packaging_level_id.code] = packaging.relative_factor
        return res

    def _format_qty_per_level(self, qty_per_level_mapping, format_pattern=None):
        """Format given qty per level mapping as string."""
        qty_per_level = self._make_qty_per_level(
            qty_per_level_mapping, format_pattern=format_pattern
        )
        res = []
        for code, qty in qty_per_level:
            res.append(f"{qty} {code}")
        return "; ".join(res)

    def _make_qty_per_level(self, qty_per_level_mapping, format_pattern=None):
        """Prepare list of packaging qty by code."""
        res = []
        format_pattern = format_pattern or "{}{}"
        for code, qty in qty_per_level_mapping.items():
            new_qty = self.relative_factor / qty
            if not new_qty.is_integer():
                new_qty_int = int(new_qty)
                new_qty_decimals = new_qty - new_qty_int
                new_qty = format_pattern.format(
                    new_qty_int, str(new_qty_decimals).lstrip("0")
                )
            res.append((code, new_qty))
        return res

    @api.onchange("package_type_id")
    def _onchange_package_type(self):
        package_type_level_id = self.package_type_id.packaging_level_id
        if package_type_level_id:
            self.packaging_level_id = package_type_level_id

    @api.depends(
        "package_type_id",
        "name_policy",
        "packaging_level_id",
        "packaging_level_id.display_name",
    )
    def _compute_name(self):
        for rec in self:
            rec.name = rec._get_name_from_policy()

    @api.depends("packaging_level_id", "name_policy")
    def _compute_display_name(self):
        super()._compute_display_name()
        for record in self:
            if record.packaging_level_id:
                record.display_name = record._get_name_from_policy(lang=self.env.lang)

    def _get_name_from_policy(self, lang=None):
        new_name = self.name
        if self.name_policy == "by_package_level":
            lang = lang or self.packaging_level_id.default_lang_id.code
            self = self.with_context(lang=lang)
            new_name = self.packaging_level_id.display_name
        elif self.name_policy == "by_package_type":
            new_name = self.package_type_id.name
        return new_name


class ProductUom(models.Model):
    _inherit = "product.uom"

    barcode_required_for_gtin = fields.Boolean(
        related="uom_id.barcode_required_for_gtin"
    )
    packaging_level_id = fields.Many2one(related="uom_id.packaging_level_id")
