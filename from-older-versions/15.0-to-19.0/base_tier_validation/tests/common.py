# Copyright 2018-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import Command
from odoo.orm.model_classes import add_to_registry
from odoo.tests import new_test_user

from odoo.addons.base.tests.common import BaseCommon


class CommonTierValidation(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from .tier_validation_tester import (
            TierDefinition,
            TierValidationTester,
            TierValidationTester2,
        )

        model_defs = (TierValidationTester, TierValidationTester2, TierDefinition)
        for model_def in model_defs:
            add_to_registry(cls.registry, model_def)
        model_names = [model_def._name for model_def in model_defs]
        cls.registry._setup_models__(cls.env.cr, model_names)
        cls.registry.init_models(
            cls.env.cr,
            model_names[:-1],
            {"models_to_check": True},
        )
        for model_name in model_names[:-1]:
            cls.addClassCleanup(cls.registry.__delitem__, model_name)

        cls.test_model = cls.env[TierValidationTester._name]
        cls.test_model_2 = cls.env[TierValidationTester2._name]

        cls.tester_model = cls.env["ir.model"].search(
            [("model", "=", "tier.validation.tester")]
        )
        cls.tester_model_2 = cls.env["ir.model"].search(
            [("model", "=", "tier.validation.tester2")]
        )
        # Create a multi-company
        cls.main_company = cls.env.ref("base.main_company")
        cls.other_company = cls.env["res.company"].create(
            {"name": f"My Company {cls.__name__}"}
        )

        for model in (cls.tester_model, cls.tester_model_2):
            # Access record:
            cls.env["ir.model.access"].create(
                {
                    "name": f"access {model.name}",
                    "model_id": model.id,
                    "perm_read": 1,
                    "perm_write": 1,
                    "perm_create": 1,
                    "perm_unlink": 1,
                }
            )

        # Create users:
        cls.test_user_1 = new_test_user(
            cls.env, name="John", login="test1", groups="base.group_system"
        )
        cls.test_user_2 = new_test_user(cls.env, name="Mike", login="test2")
        cls.test_user_3_multi_company = new_test_user(
            cls.env,
            name="Jane",
            login="test3",
            email="jane@mycompany.example.com",
            company_ids=[Command.set([cls.main_company.id, cls.other_company.id])],
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

        # Create definition for test 19, 20
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
