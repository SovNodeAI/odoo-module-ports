# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.orm.model_classes import add_to_registry
from odoo.tests import common


class CommonBaseSequenceOption(common.TransactionCase):
    def setUp(self):
        super().setUp()

        from .base_sequence_tester import BaseSequenceTester, IrSequenceOption

        self.test_model_name = BaseSequenceTester._name
        add_to_registry(self.env.registry, BaseSequenceTester)
        add_to_registry(self.env.registry, IrSequenceOption)
        self.env.registry._setup_models__(
            self.env.cr, [self.test_model_name, "ir.sequence.option"]
        )
        self.env.registry.init_models(
            self.env.cr, [self.test_model_name], {"models_to_check": True}
        )

        self.test_model = self.env[self.test_model_name]

        self.tester_model = self.env["ir.model"].search(
            [("model", "=", "base.sequence.tester")]
        )

        # Access record:
        self.env["ir.access"].create(
            {
                "name": "access.tester",
                "model_id": self.tester_model.id,
                "operation": "crud",
            }
        )

        # Create sequence for type A and type B
        self.ir_sequence_obj = self.env["ir.sequence"]
        self.ir_sequence_obj.create(
            {
                "name": "Default Sequence",
                "code": "base.sequence.tester",
                "padding": 5,
                "prefix": "DEF/",
            }
        )
        seq_a = self.ir_sequence_obj.create(
            {
                "name": "Type A",
                "padding": 5,
                "prefix": "TYPE-A/",
            }
        )
        seq_b = self.ir_sequence_obj.create(
            {
                "name": "Type B",
                "padding": 5,
                "prefix": "TYPE-B/",
            }
        )

        # Create sequence options for model base.sequence.tester:
        self.base_sequence_obj = self.env["ir.sequence.option"]
        self.base_seq = self.base_sequence_obj.create(
            {
                "name": "Test Model",
                "model": "base.sequence.tester",
                "use_sequence_option": True,
            }
        )
        self.sequence_obj = self.env["ir.sequence.option.line"]
        self.sequence_obj.create(
            {
                "base_id": self.base_seq.id,
                "name": "Option 1",
                "filter_domain": [("test_type", "=", "a")],
                "sequence_id": seq_a.id,
            }
        )
        self.sequence_obj.create(
            {
                "base_id": self.base_seq.id,
                "name": "Option 1",
                "filter_domain": [("test_type", "=", "b")],
                "sequence_id": seq_b.id,
            }
        )

    def tearDown(self):
        if self.test_model_name in self.env.registry:
            del self.env.registry[self.test_model_name]
        return super().tearDown()
