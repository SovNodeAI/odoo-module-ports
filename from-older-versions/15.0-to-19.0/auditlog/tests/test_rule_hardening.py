# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.tests.common import TransactionCase


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
