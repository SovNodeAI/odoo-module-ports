# Copyright 2018-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.orm.model_classes import add_to_registry
from odoo.tests import common

from odoo.addons.base.tests.common import DISABLED_MAIL_CREATE_CONTEXT


class CommonTierValidation(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CREATE_CONTEXT))
        from .tier_validation_tester import (
            TierDefinition,
            TierValidationTester,
            TierValidationTester2,
        )

        model_defs = (TierValidationTester, TierValidationTester2, TierDefinition)
        for model_def in model_defs:
            add_to_registry(cls.registry, model_def)

        model_names = [
            TierValidationTester._name,
            TierValidationTester2._name,
            TierDefinition._name,
        ]
        cls.registry._setup_models__(cls.env.cr, model_names)
        cls.registry.init_models(
            cls.env.cr,
            model_names,
            {"models_to_check": True},
        )
        for model_name in model_names[:2]:
            cls.addClassCleanup(cls.registry.__delitem__, model_name)

        cls.test_model = cls.env[TierValidationTester._name]
        cls.test_model_2 = cls.env[TierValidationTester2._name]

        cls.tester_model = cls.env["ir.model"].search(
            [("model", "=", "tier.validation.tester")]
        )
        cls.tester_model_2 = cls.env["ir.model"].search(
            [("model", "=", "tier.validation.tester2")]
        )

        # Access record:
        cls.env["ir.access"].create(
            {
                "name": "access.tester",
                "model_id": cls.tester_model.id,
                "group_id": cls.env.ref("base.group_everyone").id,
                "operation": "crud",
            }
        )
        cls.env["ir.access"].create(
            {
                "name": "access.tester2",
                "model_id": cls.tester_model_2.id,
                "group_id": cls.env.ref("base.group_everyone").id,
                "operation": "crud",
            }
        )
        # Create a multi-company
        cls.main_company = cls.env.ref("base.main_company")
        cls.other_company = cls.env["res.company"].create(
            {"name": f"My Company {cls.__name__}"}
        )

        # Define views to avoid automatic views with all fields.
        for model in cls.test_model._name, cls.test_model_2._name:
            cls.env["ir.ui.view"].create(
                {
                    "model": model,
                    "name": f"Demo view for {model}",
                    "arch": """<form>
                    <header>
                        <button name="action_confirm" type="object" string="Confirm" />
                        <field name="state" widget="statusbar" />
                    </header>
                    <sheet>
                        <field name="test_field" />
                    </sheet>
                    </form>""",
                }
            )

        # Create users:
        group_ids = cls.env.ref("base.group_system").ids
        cls.test_user_1 = cls.env["res.users"].create(
            {
                "name": "John",
                "login": "test1",
                "email": "john@yourcompany.example.com",
                "group_ids": [(6, 0, group_ids)],
            }
        )
        cls.test_user_2 = cls.env["res.users"].create(
            {"name": "Mike", "login": "test2", "email": "mike@yourcompany.example.com"}
        )
        cls.test_user_3_multi_company = cls.env["res.users"].create(
            {
                "name": "Jane",
                "login": "test3",
                "email": "jane@mycompany.example.com",
                "company_ids": [(6, 0, [cls.main_company.id, cls.other_company.id])],
            }
        )

        # Create tier definitions:
        cls.tier_def_obj = cls.env["tier.definition"]
        cls.tier_definition = cls.tier_def_obj.create(
            {
                "model_id": cls.tester_model.id,
                "review_type": "individual",
                "reviewer_id": cls.test_user_1.id,
                "definition_domain": "[('test_field', '>', 1.0)]",
                "sequence": 30,
            }
        )

        cls.test_record = cls.test_model.create({"test_field": 2.5})
        cls.test_record_2 = cls.test_model_2.create({"test_field": 2.5})

        # Create definition for test 28, 29
        # Main company tier definition
        cls.tier_def_obj.create(
            {
                "model_id": cls.tester_model_2.id,
                "review_type": "individual",
                "reviewer_id": cls.test_user_1.id,
                "definition_domain": "[('test_field', '>=', 1.0)]",
                "approve_sequence": True,
                "sequence": 30,
                "name": "Definition for test 30 - sequence - user 1 - main company",
                "company_id": cls.main_company.id,
            }
        )
        cls.tier_def_obj.create(
            {
                "model_id": cls.tester_model_2.id,
                "review_type": "individual",
                "reviewer_id": cls.test_user_3_multi_company.id,
                "definition_domain": "[('test_field', '>=', 1.0)]",
                "approve_sequence": True,
                "sequence": 20,
                "name": "Definition for test 30 - sequence - user 3 - main company",
                "company_id": cls.main_company.id,
            }
        )
        # Other company tier definition
        cls.tier_def_obj.create(
            {
                "model_id": cls.tester_model_2.id,
                "review_type": "individual",
                "reviewer_id": cls.test_user_3_multi_company.id,
                "definition_domain": "[('test_field', '>=', 1.0)]",
                "approve_sequence": True,
                "sequence": 30,
                "name": "Definition for test 30 - sequence - user 3 - other company",
                "company_id": cls.other_company.id,
            }
        )

    @classmethod
    def tearDownClass(cls):
        return super(CommonTierValidation, cls).tearDownClass()
