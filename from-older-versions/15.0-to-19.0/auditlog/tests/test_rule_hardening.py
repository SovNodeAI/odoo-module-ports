# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api
from odoo.tests.common import TransactionCase, tagged


class TestAuditlogRuleHardening(TransactionCase):
    def test_subscribed_rule_fields_are_readonly(self):
        """A subscribed rule cannot be edited in its form.

        Until 16.0 the fields carried states={"subscribed": [("readonly", True)]};
        that field parameter is gone, so the form view has to say it.
        """
        view = self.env.ref("auditlog.view_auditlog_rule_form")
        arch = etree.fromstring(
            self.env["auditlog.rule"].get_view(view.id, "form")["arch"]
        )
        field_names = {
            "name",
            "model_id",
            "log_read",
            "log_write",
            "log_unlink",
            "log_create",
            "log_export_data",
            "log_type",
            "users_to_exclude_ids",
            "fields_to_exclude_ids",
            "capture_record",
        }
        for field_name in field_names:
            node = arch.xpath(f"//field[@name='{field_name}']")[0]
            self.assertEqual(
                node.get("readonly"), "state == 'subscribed'", field_name
            )

    def test_rules_created_together_all_log(self):
        """Two subscribed rules created in one call both log from then on."""
        category_model = self.env.ref("base.model_res_partner_category")
        industry_model = self.env.ref("base.model_res_partner_industry")
        rules = self.env["auditlog.rule"].create(
            [
                {
                    "name": "Partner tags",
                    "model_id": category_model.id,
                    "log_create": True,
                    "state": "subscribed",
                },
                {
                    "name": "Partner industries",
                    "model_id": industry_model.id,
                    "log_create": True,
                    "state": "subscribed",
                },
            ]
        )
        self.addCleanup(rules.unlink)
        category = self.env["res.partner.category"].create({"name": "Audited tag"})
        industry = self.env["res.partner.industry"].create(
            {"name": "Audited industry"}
        )
        for model, record in ((category_model, category), (industry_model, industry)):
            self.assertEqual(
                self.env["auditlog.log"].search_count(
                    [
                        ("model_id", "=", model.id),
                        ("method", "=", "create"),
                        ("res_id", "=", record.id),
                    ]
                ),
                1,
                model.model,
            )


@tagged("post_install", "-at_install")
class TestAuditlogVirtualRecords(TransactionCase):
    def test_onchange_in_a_form_logs_no_read(self):
        """Editing a field in the form of an audited record adds no read log.

        Since 17.0 the web client's onchange reads the form's virtual record
        through web_read(); that is not a read of stored data.
        """
        industry_model = self.env.ref("base.model_res_partner_industry")
        rule = self.env["auditlog.rule"].create(
            {
                "name": "Partner industries, reads",
                "model_id": industry_model.id,
                "log_read": True,
                "log_create": False,
                "log_write": False,
                "log_unlink": False,
                "state": "subscribed",
            }
        )
        self.addCleanup(rule.unlink)
        industry = self.env["res.partner.industry"].create({"name": "Audited"})
        domain = [
            ("model_id", "=", industry_model.id),
            ("method", "=", "read"),
            ("res_id", "=", industry.id),
        ]
        industry.read(["name"])
        logged = self.env["auditlog.log"].search_count(domain)
        self.assertEqual(logged, 1, "a read of the stored record is logged")
        # the name changes the display name: the client is sent the new one,
        # which Odoo reads from the form's virtual record
        result = industry.onchange(
            {"name": "Audited, renamed", "display_name": "Audited"},
            ["name"],
            {"name": {}, "display_name": {}},
        )
        self.assertEqual(result["value"], {"display_name": "Audited, renamed"})
        self.assertEqual(self.env["auditlog.log"].search_count(domain), logged)


class TestAuditlogForeignPatches(TransactionCase):
    def test_removing_a_rule_keeps_patches_of_other_modules(self):
        """A rule that never hooked a method leaves that method alone.

        base_automation patches create / write / unlink on the model class and
        gives its patch an "origin", exactly as auditlog does.
        """
        industry_model = self.env.ref("base.model_res_partner_industry")
        model_class = self.env.registry["res.partner.industry"]

        @api.model_create_multi
        def create(self, vals_list):
            return create.origin(self, vals_list)

        create.origin = model_class.create
        model_class.create = create

        def restore():
            if model_class.__dict__.get("create") is create:
                del model_class.create

        self.addCleanup(restore)
        rule = self.env["auditlog.rule"].create(
            {"name": "Never subscribed", "model_id": industry_model.id}
        )
        self.assertTrue(rule.log_create)
        rule.unlink()
        self.assertIs(model_class.__dict__.get("create"), create)
