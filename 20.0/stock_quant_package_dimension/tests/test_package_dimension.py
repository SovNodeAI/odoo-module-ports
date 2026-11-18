# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.tests import Form

from . import common


class TestStockQuantPackageProductPackaging(common.TestStockQuantPackageCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # In Odoo 20 a product packaging is a UoM available on the product
        cls.product.uom_ids = cls.packaging = cls.env["uom.uom"].create(
            {
                "name": "10 pack",
                "relative_factor": 10,
                "relative_uom_id": cls.env.ref("uom.product_uom_unit").id,
                "packaging_length": 12,
                "width": 13,
                "height": 14,
                "weight": 15,
            }
        )
        cls.uom_cm = cls.env["uom.uom"].search([("name", "=", "cm")], limit=1)

    def test_set_dimensions_on_write(self):
        self.package.with_context(
            _auto_assign_packaging=True
        ).product_packaging_id = self.packaging
        self.assertRecordValues(
            self.package,
            [{"pack_length": 12, "width": 13, "height": 14, "pack_weight": 15}],
        )

    def test_set_dimensions_on_write_no_override(self):
        values = {"pack_length": 22, "width": 23, "height": 24, "pack_weight": 25}
        self.package.write(values)
        self.package.with_context(
            _auto_assign_packaging=True
        ).product_packaging_id = self.packaging
        self.assertRecordValues(self.package, [values])

    def test_set_dimensions_onchange(self):
        values = {"pack_length": 22, "width": 23, "height": 24, "pack_weight": 25}
        self.package.write(values)
        with Form(self.package) as form:
            form.product_packaging_id = self.packaging
            form.save()
        # onchange overrides values
        self.assertRecordValues(
            self.package,
            [{"pack_length": 12, "width": 13, "height": 14, "pack_weight": 15}],
        )
