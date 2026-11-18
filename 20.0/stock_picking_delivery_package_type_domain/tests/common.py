# Copyright 2024 ACSONE SA/NV (https://www.acsone.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from types import SimpleNamespace
from unittest import mock

from odoo import models
from odoo.fields import Command


class FakeModelLoader:
    """Load test model extensions using the Odoo 20 registry API."""

    def __init__(self, env, module):
        self.env = env
        self._module_name = module.split(".")[2]

    @property
    def module_to_models(self):
        return models.MetaModel._module_to_models__

    def backup_registry(self):
        self._original_registry = {
            name: {
                "base": model.__bases__,
                "base_classes": model._base_classes__,
                "fields": model._fields,
                "field_definitions": model._fields__,
                "inherit_module": model._inherit_module.copy(),
                "inherit_children": model._inherit_children.copy(),
                "inherits_children": model._inherits_children.copy(),
            }
            for name, model in self.env.registry.models.items()
        }
        self._original_module_to_models = {
            key: list(model_classes)
            for key, model_classes in self.module_to_models.items()
        }

    def _clean_module_to_model(self):
        for key, model_classes in self._original_module_to_models.items():
            self.module_to_models[key] = list(model_classes)
        for key in self.module_to_models.keys() - self._original_module_to_models:
            del self.module_to_models[key]

    def update_registry(self, odoo_models):
        self.env.flush_all()
        self._clean_module_to_model()
        for model in odoo_models:
            if model not in self.module_to_models[self._module_name]:
                self.module_to_models[self._module_name].append(model)

        with (
            mock.patch.object(self.env.cr, "commit"),
            mock.patch.object(self.env.registry, "ready", False),
        ):
            self.env.registry.loaded_xmlids = set()
            module = SimpleNamespace(name=self._module_name)
            model_names = self.env.registry.load(module)
            self.env.registry._setup_models__(self.env.cr, model_names)
            self.env.registry.init_models(
                self.env.cr, model_names, {"module": self._module_name}
            )

    def restore_registry(self):
        for name, original in self._original_registry.items():
            model = self.env.registry[name]
            model.__bases__ = original["base"]
            model._base_classes__ = original["base_classes"]
            model._fields = original["fields"]
            model._fields__ = original["field_definitions"]
            model._inherit_module = original["inherit_module"]
            model._inherit_children = original["inherit_children"]
            model._inherits_children = original["inherits_children"]
            for field in model._fields:
                if not field.startswith("x_") and field in vars(model):
                    delattr(model, field)

        for name in self.env.registry.models.keys() - self._original_registry:
            del self.env.registry.models[name]

        self._clean_module_to_model()
        self.env.invalidate_all(flush=False)


class CommonChooseDeliveryPackage:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "is_storable": True,
            }
        )

        cls.env["stock.quant"].with_context(inventory_mode=True).create(
            {
                "product_id": cls.product.id,
                "location_id": cls.env.ref("stock.stock_location_stock").id,
                "inventory_quantity": 10.0,
            }
        )._apply_inventory()

    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()

        from .models.test import DeliveryCarrier, StockPackageType

        self.loader.update_registry((DeliveryCarrier, StockPackageType))

        self.delivery_obj = self.env["delivery.carrier"]
        self.package_type_obj = self.env["stock.package.type"]
        self.package_type = self.package_type_obj.create(
            {
                "name": "Type Test",
                "package_carrier_type": "test",
            }
        )
        self.product_delivery = self.env["product.product"].create(
            {
                "name": "Delivery Product",
                "type": "service",
            }
        )
        self.delivery = self.delivery_obj.create(
            {
                "name": "Test",
                "delivery_type": "test",
                "product_id": self.product_delivery.id,
            }
        )

    def _create_sale(self):
        self.sale = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "carrier_id": self.delivery.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 5.0,
                        }
                    )
                ],
            }
        )
        return self.sale

    def tearDown(self):
        self.loader.restore_registry()
        self.env = self.env(su=True)
        super().tearDown()
