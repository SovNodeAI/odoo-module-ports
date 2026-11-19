/**
 * Copyright 2026 SovNode AI
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
 */
import {describe, expect, test} from "@odoo/hoot";
import {click, waitFor} from "@odoo/hoot-dom";
import {defineMailModels} from "@mail/../tests/mail_test_helpers";
import {defineModels, fields, models, mountView} from "@web/../tests/web_test_helpers";

describe.current.tags("desktop");

const CHART = JSON.stringify({
    div: '<div class="o_test_ddmrp_chart">chart</div>',
    script: "",
});

class StockBuffer extends models.Model {
    _name = "stock.buffer";
    _rec_name = "display_name";

    display_name = fields.Char();
    on_hand_percent = fields.Float();
    execution_priority_level = fields.Selection({
        selection: [
            ["0_grey", "Grey"],
            ["1_red", "Red"],
            ["2_yellow", "Yellow"],
            ["3_green", "Green"],
        ],
    });
    ddmrp_chart_execution = fields.Text();

    _records = [
        {
            id: 1,
            display_name: "Buffer A",
            on_hand_percent: 42,
            execution_priority_level: "1_red",
            ddmrp_chart_execution: CHART,
        },
    ];
}

defineMailModels();
defineModels([StockBuffer]);

const ARCH = `<list>
    <field name="display_name"/>
    <field name="execution_priority_level" column_invisible="1"/>
    <field
        name="on_hand_percent"
        options='{"color_from": "execution_priority_level", "field": "ddmrp_chart_execution"}'
        widget="stock_buffer_info"
    />
</list>`;

test("stock_buffer_info widget renders the buffer decoration", async () => {
    await mountView({type: "list", resModel: "stock.buffer", arch: ARCH});
    expect("span.circle").toHaveCount(1);
    expect("span.circle").toHaveClass("circle_red");
    expect("span.circle").toHaveText("42.00");
});

test("stock_buffer_info widget opens the buffer chart popover", async () => {
    await mountView({type: "list", resModel: "stock.buffer", arch: ARCH});
    await click("span.circle");
    await waitFor(".o_popover .stock-buffer-popover .o_test_ddmrp_chart");
    expect(".o_popover .stock-buffer-popover .o_test_ddmrp_chart").toHaveCount(1);
});
