# Copyright 2026 SovNode AI
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

import ast
from datetime import datetime
from types import SimpleNamespace
from lxml import html
from xml.etree import ElementTree

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import common


class TestPurchaseRequestPortRegressions(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env["res.partner"].create({"name": "Regression Supplier"})
        cls.unit = cls.env.ref("uom.product_uom_unit")
        cls.dozen = cls.env.ref("uom.product_uom_dozen")
        cls.product = cls.env["product.product"].create(
            {"name": "Regression Product", "purchase_ok": True}
        )
        cls.purchase_request_model = cls.env["purchase.request"]
        cls.purchase_request_line_model = cls.env["purchase.request.line"]
        cls.wizard_model = cls.env["purchase.request.line.make.purchase.order"]

    def _create_request(self, product=None, date_required=False):
        return self.purchase_request_model.create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_in").id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": (product or self.product).id,
                            "name": "Regression request line",
                            "product_qty": 1.0,
                            "product_uom_id": self.unit.id,
                            "date_required": date_required or fields.Date.today(),
                        },
                    )
                ],
            }
        )

    def _create_wizard(self, request, **values):
        return self.wizard_model.with_context(
            active_model="purchase.request.line",
            active_ids=request.line_ids.ids,
        ).create({"supplier_id": self.supplier.id, **values})

    def test_form_chatter_icons_and_kanban_layout(self):
        for xml_id in (
            "purchase_request.view_purchase_request_form",
            "purchase_request.purchase_request_line_form",
        ):
            arch = ElementTree.fromstring(self.env.ref(xml_id).arch)
            self.assertEqual(len(arch.findall("chatter")), 1)
            self.assertFalse(arch.findall(".//div[@class='oe_chatter']"))

        for xml_id in (
            "purchase_request.view_purchase_request_form",
            "purchase_request.view_purchase_request_search",
            "purchase_request.purchase_order_form",
            "purchase_request.purchase_order_line_tree",
        ):
            record = self.env.ref(xml_id)
            for element in ElementTree.fromstring(record.arch).iter():
                if "icon" in element.attrib:
                    self.assertRegex(element.attrib["icon"], r"^(fa|oi)-")

        kanban = ElementTree.fromstring(
            self.env.ref("purchase_request.view_purchase_request_kanban").arch
        )
        card = kanban.find(".//t[@t-name='card']")
        self.assertIsNotNone(card.find("footer"))
        self.assertEqual(card[0].get("class"), "d-flex justify-content-between mb-3")
        for element in card.iter():
            self.assertNotIn("oe_kanban_card", element.get("class", ""))
            self.assertNotIn("o_kanban_record_top", element.get("class", ""))
            self.assertNotIn("o_kanban_record_bottom", element.get("class", ""))

    def test_duplicate_several_requests_in_one_call(self):
        """The list view's Duplicate action copies every selected request at once."""
        requests = self._create_request() + self._create_request()
        requests.button_to_approve()
        copies = requests.copy()
        self.assertEqual(len(copies), 2)
        self.assertEqual(copies.mapped("state"), ["draft", "draft"])
        names = requests.mapped("name") + copies.mapped("name")
        self.assertEqual(len(set(names)), 4, "every copy gets a number of its own")
        self.assertEqual(len(copies.line_ids), 2)
        # one request alone still gives what the original gave
        single = requests[0].copy()
        self.assertEqual(single.state, "draft")
        self.assertNotIn(single.name, names)

    def test_procurement_allows_false_destination_moves(self):
        request = self._create_request()
        procurement = SimpleNamespace(
            product_id=self.product,
            product_qty=2.0,
            product_uom=self.unit,
            values={
                "date_planned": fields.Datetime.now(),
                "move_dest_ids": False,
                "orderpoint_id": False,
            },
        )
        vals = self.env["stock.rule"]._prepare_purchase_request_line(
            request, procurement
        )
        self.assertEqual(vals["move_dest_ids"], [])
        self.assertTrue(self.purchase_request_line_model.create(vals))

    def test_view_membership_expressions_use_sequences(self):
        expression_count = 0
        for xml_id in (
            "purchase_request.purchase_request_line_tree",
            "purchase_request.purchase_request_line_form",
            "purchase_request.view_purchase_request_form",
            "purchase_request.view_purchase_request_tree",
        ):
            arch = ElementTree.fromstring(self.env.ref(xml_id).arch)
            for element in arch.iter():
                for attribute, expression in element.attrib.items():
                    if not any(operator in expression for operator in (" in ", " not in ")):
                        continue
                    for node in ast.walk(ast.parse(expression, mode="eval")):
                        if isinstance(node, ast.Compare) and any(
                            isinstance(operator, (ast.In, ast.NotIn))
                            for operator in node.ops
                        ):
                            expression_count += 1
                            self.assertIsInstance(
                                node.comparators[0],
                                (ast.Tuple, ast.List, ast.Set, ast.Dict),
                                f"{xml_id} {attribute}: {expression}",
                            )
        self.assertGreater(expression_count, 0)

    def test_analytic_grouping_and_multi_plan_report(self):
        plan_model = self.env["account.analytic.plan"]
        account_model = self.env["account.analytic.account"]
        plan1 = plan_model.create({"name": "Regression Plan 1"})
        plan2 = plan_model.create({"name": "Regression Plan 2"})
        account1 = account_model.create({"name": "Project A", "plan_id": plan1.id})
        account2 = account_model.create({"name": "Project B", "plan_id": plan2.id})
        request = self._create_request()
        request.line_ids.analytic_distribution = {
            f"{account1.id},{account2.id}": 100.0
        }
        self.assertEqual(
            request.line_ids._get_analytic_name(),
            ["Project A, Project B (100.0)"],
        )
        request.line_ids.analytic_distribution = {str(account1.id): 100.0}
        self.assertEqual(
            request.line_ids._get_analytic_name(), ["Project A (100.0)"]
        )
        self.assertEqual(
            request.line_ids._get_analytic_distribution(), "Project A (100.0)"
        )
        # Grouping request lines by analytic distribution is not offered: Odoo 19's
        # analytic mixin supports it for four of its own models, and with the record
        # count only (addons/analytic/models/analytic_mixin.py, _get_count_id and
        # _read_group_select), while a list view also asks for sums.
        search_view = self.env.ref("purchase_request.purchase_request_line_search")
        arch = self.purchase_request_line_model.get_view(search_view.id, "search")[
            "arch"
        ]
        group_bys = [
            node.get("context")
            for node in ElementTree.fromstring(arch).iter("filter")
            if "group_by" in (node.get("context") or "")
        ]
        self.assertTrue(group_bys)
        self.assertFalse([c for c in group_bys if "analytic_distribution" in c])

        def rendered_analytic_names():
            report = self.env["ir.actions.report"]._render_qweb_html(
                "purchase_request.report_purchase_request", request.ids
            )
            table = html.fromstring(report[0]).find(".//tbody")
            return [
                " ".join(cell.itertext()).strip() for cell in table[0].findall("td")
            ]

        self.env.user.group_ids |= self.env.ref(
            "analytic.group_analytic_accounting"
        )
        self.assertEqual(rendered_analytic_names()[1], "Project A (100.0)")
        request.line_ids.analytic_distribution = {
            f"{account1.id},{account2.id}": 100.0
        }
        self.assertEqual(
            rendered_analytic_names()[1], "Project A, Project B (100.0)"
        )

    def test_supplier_minimum_is_converted_from_the_vendor_unit(self):
        """A vendor minimum of 5 dozen means 60 units on a purchase line in units."""
        product = self.env["product.product"].create(
            {"name": "Vendor Dozen Product", "purchase_ok": True}
        )
        self.env["product.supplierinfo"].create(
            {
                "partner_id": self.supplier.id,
                "product_tmpl_id": product.product_tmpl_id.id,
                "product_uom_id": self.dozen.id,
                "min_qty": 5.0,
            }
        )
        line_model = self.purchase_request_line_model
        self.assertEqual(
            line_model._get_supplier_min_qty(product, self.supplier), 60.0
        )
        self.assertEqual(
            line_model._get_supplier_min_qty(product, self.supplier, self.dozen), 5.0
        )
        request = self._create_request(product=product)
        request.button_approved()
        wizard = self._create_wizard(request)
        wizard.make_purchase_order()
        po_line = request.line_ids.purchase_lines
        self.assertEqual(po_line.product_uom_id, self.unit)
        self.assertEqual(po_line.product_qty, 60.0)
        # a second request for the same product joins the line; the minimum still holds
        request2 = self._create_request(product=product)
        request2.button_approved()
        wizard2 = self._create_wizard(
            request2, purchase_order_id=po_line.order_id.id
        )
        wizard2.make_purchase_order()
        self.assertEqual(po_line.product_qty, 60.0)

    def test_supplier_minimum_in_the_product_unit_is_unchanged(self):
        """With the vendor price in the product's own unit nothing is converted."""
        product = self.env["product.product"].create(
            {"name": "Vendor Unit Product", "purchase_ok": True}
        )
        self.env["product.supplierinfo"].create(
            {
                "partner_id": self.supplier.id,
                "product_tmpl_id": product.product_tmpl_id.id,
                "min_qty": 5.0,
            }
        )
        request = self._create_request(product=product)
        request.button_approved()
        self._create_wizard(request).make_purchase_order()
        self.assertEqual(request.line_ids.purchase_lines.product_qty, 5.0)

    def test_sync_date_planned_uses_same_timezone_conversion(self):
        self.env.user.tz = "Asia/Bangkok"
        required_date = fields.Date.to_date("2030-01-02")
        request1 = self._create_request(date_required=required_date)
        request1.button_approved()
        self._create_wizard(request1).make_purchase_order()
        po = request1.line_ids.purchase_lines.order_id
        self.assertEqual(po.order_line.date_planned, datetime(2030, 1, 1, 17))

        request2 = self._create_request(date_required=required_date)
        request2.button_approved()
        wizard = self._create_wizard(
            request2, purchase_order_id=po.id, sync_data_planned=True
        )
        wizard.make_purchase_order()
        self.assertEqual(len(po.order_line), 1)
        self.assertEqual(po.order_line.product_qty, 2.0)
        self.assertEqual(
            po.order_line.purchase_request_lines, request1.line_ids | request2.line_ids
        )

    def test_wizard_keeps_ids_api_and_allows_product_choice(self):
        request = self._create_request()
        with self.assertRaises(UserError):
            self.wizard_model.with_context(
                active_model="purchase.request.line", active_ids=request.line_ids.ids
            ).create({"supplier_id": self.supplier.id})
        request.button_approved()
        wizard = self._create_wizard(request)
        self.assertEqual(wizard.item_ids.line_id, request.line_ids)
        wizard._check_valid_request_line(request.line_ids.ids)

        other_product = self.env["product.product"].create(
            {"name": "Wizard Selected Product", "purchase_ok": True}
        )
        wizard.item_ids.product_id = other_product
        wizard.make_purchase_order()
        self.assertEqual(wizard.item_ids.line_id.product_id, other_product)
        self.assertEqual(len(wizard.item_ids.line_id.purchase_lines), 1)
