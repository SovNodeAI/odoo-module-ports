# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from lxml import etree

from odoo.fields import Command
from odoo.tests import tagged
from odoo.tools.safe_eval import safe_eval

from .common import TestAutomaticWorkflowMixin, TestCommon


@tagged("post_install", "-at_install")
class TestRegressions(TestCommon, TestAutomaticWorkflowMixin):
    def setUp(self):
        super().setUp()
        self.env = self.env(
            context=dict(
                self.env.context,
                tracking_disable=True,
                _job_force_sync=True,
            )
        )

    def _create_paid_workflow_order(self):
        workflow = self.create_full_automatic(override={"register_payment": True})
        sale = self.create_sale_order(workflow)
        self.run_job()
        invoice = sale.invoice_ids
        self.assertEqual(invoice.state, "posted")
        return sale, invoice

    def _payment_count(self, sale):
        return self.env["account.payment"].search_count(
            [("partner_id", "=", sale.partner_id.id)]
        )

    def test_register_payment_only_once(self):
        """Running the job twice must not pay the same invoice twice."""
        sale, invoice = self._create_paid_workflow_order()
        self.assertEqual(self._payment_count(sale), 1)
        self.run_job()
        self.run_job()
        self.assertEqual(self._payment_count(sale), 1)
        self.assertEqual(invoice.payment_state, "paid")

    def test_register_payment_only_once_in_payment_state(self):
        """With Accounting installed the invoice stays 'in_payment' while its
        residual amount is still the full total: the job must not pay it again.
        """
        with patch.object(
            self.env.registry["account.move"],
            "_get_invoice_in_payment_state",
            return_value="in_payment",
        ):
            sale, invoice = self._create_paid_workflow_order()
            self.assertEqual(invoice.payment_state, "in_payment")
            self.assertEqual(self._payment_count(sale), 1)
            self.run_job()
            self.run_job()
            self.assertEqual(self._payment_count(sale), 1)

    def test_register_payment_skips_zero_residual_invoice(self):
        """An invoice with nothing left to pay gets no payment."""
        workflow = self.create_full_automatic(override={"register_payment": True})
        product = self.env["product.product"].create(
            {"name": "Free", "list_price": 0.0, "type": "consu"}
        )
        self.product_uom_unit = self.env.ref("uom.product_uom_unit")
        sale = self.create_sale_order(
            workflow,
            override={
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": product.name,
                            "product_id": product.id,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 0.0,
                            "product_uom_qty": 1,
                        },
                    )
                ]
            },
        )
        self.run_job()
        invoice = sale.invoice_ids
        self.assertEqual(invoice.state, "posted")
        self.assertTrue(invoice.currency_id.is_zero(invoice.amount_residual))
        payment = self.env["automatic.workflow.job"]._register_payment_invoice(invoice)
        self.assertFalse(payment)
        self.assertEqual(self._payment_count(sale), 0)

    def test_all_qty_delivered_uses_product_unit_precision(self):
        """The 'Product Unit' precision (3 digits) must be honoured."""
        self.env["decimal.precision"].search(
            [("name", "=", "Product Unit")]
        ).write({"digits": 3})
        workflow = self.create_full_automatic()
        sale = self.create_sale_order(workflow)
        sale.order_line.write({"qty_delivered": 0.996})
        self.assertFalse(sale.all_qty_delivered)
        sale.order_line.write({"qty_delivered": 1.0})
        self.assertTrue(sale.all_qty_delivered)

    def test_all_qty_delivered_ignores_combo_line(self):
        """A combo parent line never gets a delivery and must be ignored, but
        the combo item line it carries must still be delivered."""
        combo_item_product = self.env["product.product"].create(
            {"name": "Combo choice", "list_price": 5.0, "type": "consu"}
        )
        combo = self.env["product.combo"].create(
            {
                "name": "Combo",
                "combo_item_ids": [
                    Command.create({"product_id": combo_item_product.id})
                ],
            }
        )
        combo_product = self.env["product.product"].create(
            {
                "name": "Combo product",
                "list_price": 5.0,
                "type": "combo",
                "combo_ids": [Command.link(combo.id)],
            }
        )
        workflow = self.create_full_automatic()
        self.product_uom_unit = self.env.ref("uom.product_uom_unit")
        sale = self.create_sale_order(
            workflow,
            override={
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": combo_product.name,
                            "product_id": combo_product.id,
                            "product_uom_id": self.product_uom_unit.id,
                            "product_uom_qty": 1,
                        },
                    )
                ]
            },
        )
        parent_line = sale.order_line
        self.assertEqual(parent_line.product_id.type, "combo")
        self.assertEqual(parent_line.qty_delivered, 0.0)
        child_line = self.env["sale.order.line"].create(
            {
                "order_id": sale.id,
                "product_id": combo_item_product.id,
                "product_uom_id": self.product_uom_unit.id,
                "product_uom_qty": 1,
                "combo_item_id": combo.combo_item_ids.id,
                "linked_line_id": parent_line.id,
            }
        )
        self.assertEqual(child_line.qty_delivered, 0.0)
        self.assertFalse(sale.all_qty_delivered)
        child_line.write({"qty_delivered": 1.0})
        self.assertTrue(sale.all_qty_delivered)

    def test_register_payment_with_credit_journal(self):
        """A 'credit' journal is a valid payment journal and must be used."""
        workflow = self.create_full_automatic(override={"register_payment": True})
        credit_journal = self.env["account.journal"].create(
            {"name": "Credit Card", "code": "CCARD", "type": "credit"}
        )
        workflow.property_payment_journal_id = credit_journal
        sale = self.create_sale_order(workflow)
        self.run_job()
        payment = self.env["account.payment"].search(
            [("partner_id", "=", sale.partner_id.id)]
        )
        self.assertEqual(len(payment), 1)
        self.assertEqual(payment.journal_id, credit_journal)
        self.assertEqual(sale.invoice_ids.payment_state, "paid")

    def test_register_payment_skips_blocked_invoice(self):
        """A blocked invoice must never be paid by the cron."""
        workflow = self.create_full_automatic()
        sale = self.create_sale_order(workflow)
        self.run_job()
        invoice = sale.invoice_ids
        self.assertEqual(invoice.state, "posted")
        invoice.action_toggle_block_payment()
        self.assertEqual(invoice.payment_state, "blocked")
        workflow.register_payment = True
        self.run_job()
        self.run_job()
        self.assertEqual(invoice.payment_state, "blocked")
        self.assertEqual(self._payment_count(sale), 0)
        # Even when the payment filter is widened by the user, the job must
        # not pay an invoice the user blocked.
        payment = self.env["automatic.workflow.job"]._register_payment_invoice(invoice)
        self.assertFalse(payment)
        self.assertEqual(self._payment_count(sale), 0)

    def test_sale_done_filter_skips_locked_order(self):
        """The cron filters must not select orders that are already locked,
        otherwise every run locks them again."""
        workflow = self.create_full_automatic(override={"sale_done": True})
        sale = self.create_sale_order(workflow)
        self.run_job()
        self.assertTrue(sale.locked)
        sale_done_domain = safe_eval(workflow.sale_done_filter_id.domain)
        self.assertNotIn(sale, self.env["sale.order"].search(sale_done_domain))

        # Same for the create invoice filter: a locked order still waiting for
        # its invoice must not be invoiced by the cron.
        sale2 = self.create_sale_order(workflow)
        sale2.action_confirm()
        sale2.action_lock()
        self.assertEqual(sale2.invoice_status, "to invoice")
        create_domain = safe_eval(workflow.create_invoice_filter_id.domain)
        self.assertNotIn(sale2, self.env["sale.order"].search(create_domain))

    def test_property_journal_id_accepts_sale_journal(self):
        """The Sales Journal field must offer the sale journals, the only
        journals an invoice can be created in."""
        view = self.env["sale.workflow.process"].get_view(view_type="form")
        arch = etree.fromstring(view["arch"])
        field = arch.xpath("//field[@name='property_journal_id']")[0]
        domain = safe_eval(field.get("domain") or "[]")
        sale_journal = self.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        bank_journal = self.env["account.journal"].search(
            [("type", "=", "bank")], limit=1
        )
        self.assertTrue(sale_journal)
        self.assertTrue(bank_journal)
        self.assertIn(
            sale_journal, self.env["account.journal"].search(domain)
        )
        self.assertNotIn(
            bank_journal, self.env["account.journal"].search(domain)
        )
