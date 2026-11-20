// Copyright 2026 Tecnativa - Carlos Roca
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import { expect, test } from "@odoo/hoot";
import { waitFor } from "@odoo/hoot-dom";
import { defineMailModels } from "@mail/../tests/mail_test_helpers";
import {
    contains,
    defineModels,
    fields,
    models,
    mountView,
} from "@web/../tests/web_test_helpers";

class UomUom extends models.Model {
    _name = "uom.uom";

    name = fields.Char();
    factor = fields.Float();

    _records = [
        { id: 1, name: "Units", factor: 1 },
        { id: 2, name: "Dozens", factor: 12 },
    ];
}

class ProductProduct extends models.Model {
    _name = "product.product";

    name = fields.Char();
    uom_id = fields.Many2one({ relation: "uom.uom" });

    _records = [{ id: 1, name: "Test Product", uom_id: 1 }];
}

class StockMove extends models.Model {
    _name = "stock.move";
}

class StockWarehouse extends models.Model {
    _name = "stock.warehouse";

    name = fields.Char();

    _records = [{ id: 1, name: "Warehouse" }];
}

class SaleOrderLine extends models.Model {
    _name = "sale.order.line";

    name = fields.Char();
    state = fields.Selection({
        selection: [
            ["draft", "Draft"],
            ["sale", "Sales Order"],
        ],
    });
    product_id = fields.Many2one({ relation: "product.product" });
    product_uom_id = fields.Many2one({ relation: "uom.uom" });
    display_qty_widget = fields.Boolean();
    free_qty_today = fields.Float();
    forecast_expected_date = fields.Datetime();
    is_mto = fields.Boolean();
    move_ids = fields.One2many({ relation: "stock.move" });
    qty_available_today = fields.Float();
    qty_to_deliver = fields.Float();
    scheduled_date = fields.Datetime();
    virtual_available_at_date = fields.Float();
    warehouse_id = fields.Many2one({ relation: "stock.warehouse" });
    immediately_usable_qty_today = fields.Float();

    _records = [
        {
            id: 1,
            name: "Test line",
            state: "draft",
            product_id: 1,
            product_uom_id: 1,
            display_qty_widget: true,
            free_qty_today: 5,
            is_mto: false,
            move_ids: [],
            qty_available_today: 0,
            qty_to_deliver: 3,
            scheduled_date: "2026-11-20 10:00:00",
            virtual_available_at_date: 10,
            warehouse_id: 1,
            immediately_usable_qty_today: 42,
        },
    ];
}

defineModels([UomUom, ProductProduct, StockMove, StockWarehouse, SaleOrderLine]);
defineMailModels();

test("qty at date popover shows the available to promise quantity", async () => {
    await mountView({
        type: "form",
        resModel: "sale.order.line",
        resId: 1,
        arch: /* xml */ `
            <form>
                <field name="state" invisible="1"/>
                <field name="product_uom_id" invisible="1"/>
                <widget name="qty_at_date_widget"/>
            </form>`,
    });
    expect(".o_widget_qty_at_date_widget a").toHaveCount(1);
    await contains(".o_widget_qty_at_date_widget a").click();
    await waitFor(".o_popover");
    expect(".o_popover tbody tr:first-child strong").toHaveText("Available to promise");
    expect(".o_popover tbody tr:first-child td.text-end b").toHaveText("42");
});
