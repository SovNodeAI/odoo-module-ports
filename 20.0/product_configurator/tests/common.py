from odoo.addons.base.tests.common import BaseCommon
from odoo.tools import convert_file


class ProductConfiguratorTestCases(BaseCommon):
    # The module's access checks rely on the manager group; run as superuser
    # like the original Odoo 18 tests did.
    _test_user_groups = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_module_demo_data(cls.env)
        cls.ProductConfWizard = cls.env["product.configurator"]
        cls.config_product = cls.env.ref("product_configurator.bmw_2_series")
        cls.product_category = cls.env.ref("product.product_category_goods")
        # attributes
        cls.attr_fuel = cls.env.ref("product_configurator.product_attribute_fuel")
        cls.attr_engine = cls.env.ref("product_configurator.product_attribute_engine")
        cls.attr_color = cls.env.ref("product_configurator.product_attribute_color")
        cls.attr_rims = cls.env.ref("product_configurator.product_attribute_rims")
        cls.attr_model_line = cls.env.ref(
            "product_configurator.product_attribute_model_line"
        )
        cls.attr_tapistry = cls.env.ref(
            "product_configurator.product_attribute_tapistry"
        )
        cls.attr_transmission = cls.env.ref(
            "product_configurator.product_attribute_transmission"
        )
        cls.attr_options = cls.env.ref("product_configurator.product_attribute_options")

        # values
        cls.value_gasoline = cls.env.ref(
            "product_configurator.product_attribute_value_gasoline"
        )
        cls.value_218i = cls.env.ref(
            "product_configurator.product_attribute_value_218i"
        )
        cls.value_220i = cls.env.ref(
            "product_configurator.product_attribute_value_220i"
        )
        cls.value_red = cls.env.ref("product_configurator.product_attribute_value_red")
        cls.value_rims_378 = cls.env.ref(
            "product_configurator.product_attribute_value_rims_378"
        )
        cls.value_sport_line = cls.env.ref(
            "product_configurator.product_attribute_value_sport_line"
        )
        cls.value_model_sport_line = cls.env.ref(
            "product_configurator.product_attribute_value_model_sport_line"
        )
        cls.value_tapistry = cls.env.ref(
            "product_configurator.product_attribute_value_tapistry" + "_oyster_black"
        )
        cls.value_transmission = cls.env.ref(
            "product_configurator.product_attribute_value_steptronic"
        )
        cls.value_options_1 = cls.env.ref(
            "product_configurator.product_attribute_value_smoker_package"
        )
        cls.value_options_2 = cls.env.ref(
            "product_configurator.product_attribute_value_sunroof"
        )

    @classmethod
    def _configure_product_nxt_step(cls):
        product_config_wizard = cls.ProductConfWizard.create(
            {
                "product_tmpl_id": cls.config_product.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                f"__attribute_{cls.attr_fuel.id}": cls.value_gasoline.id,
                f"__attribute_{cls.attr_engine.id}": cls.value_218i.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                f"__attribute_{cls.attr_color.id}": cls.value_red.id,
                f"__attribute_{cls.attr_rims.id}": cls.value_rims_378.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                f"__attribute_{cls.attr_model_line.id}": cls.value_sport_line.id,
            }
        )
        product_config_wizard.action_previous_step()
        product_config_wizard.action_previous_step()
        product_config_wizard.write(
            {
                f"__attribute_{cls.attr_engine.id}": cls.value_220i.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.action_next_step()
        vals = {
            f"__attribute_{cls.attr_model_line.id}": cls.value_model_sport_line.id,
        }
        product_config_wizard.write(vals)
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                f"__attribute_{cls.attr_tapistry.id}": cls.value_tapistry.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                f"__attribute_{cls.attr_transmission.id}": cls.value_transmission.id,
                f"__attribute_{cls.attr_options.id}": [
                    [6, 0, [cls.value_options_2.id]]
                ],
            }
        )

        return product_config_wizard.action_next_step()


# Demo data is no longer installed by default in Odoo 20 test databases,
# so the tests that rely on it load it explicitly when missing.
DEMO_FILES = [
    "demo/product_template.xml",
    "demo/product_attribute.xml",
    "demo/product_config_domain.xml",
    "demo/product_config_lines.xml",
    "demo/product_config_step.xml",
    "demo/config_image_ids.xml",
]


PRODUCT_DEMO_FILES = [
    "data/product_attribute_demo.xml",
    "data/product_category_demo.xml",
    "data/product_demo.xml",
]


def load_module_demo_data(env):
    if not env.ref("product.product_delivery_01", raise_if_not_found=False):
        for fname in PRODUCT_DEMO_FILES:
            convert_file(env, "product", fname, {}, mode="init", noupdate=True)
    if env.ref("product_configurator.bmw_2_series", raise_if_not_found=False):
        return
    for fname in DEMO_FILES:
        convert_file(env, "product_configurator", fname, {}, mode="init", noupdate=True)
