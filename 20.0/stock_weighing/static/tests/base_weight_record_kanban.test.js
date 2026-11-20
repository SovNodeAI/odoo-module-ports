/* Copyright 2026 Tecnativa - Sergio Teruel
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import {animationFrame, click, press} from "@odoo/hoot-dom";
import {
    contains,
    defineModels,
    fields,
    getKanbanColumn,
    getKwArgs,
    models,
    mountView,
} from "@web/../tests/web_test_helpers";
import {describe, expect, test} from "@odoo/hoot";
import {defineMailModels} from "@mail/../tests/mail_test_helpers";

describe.current.tags("desktop");

const PICKING_IDS = [...Array(12).keys()].map((index) => index + 1);

class Picking extends models.Model {
    name = fields.Char();

    _records = PICKING_IDS.map((id) => ({id, name: `PICK/${id}`}));
}

class Move extends models.Model {
    picking_id = fields.Many2one({relation: "picking"});

    _records = PICKING_IDS.map((id) => ({id, picking_id: id}));

    web_read_group(...args) {
        const kwargs = getKwArgs(
            args,
            "domain",
            "groupby",
            "aggregates",
            "limit",
            "offset",
            "order",
            "auto_unfold",
            "opening_info",
            "unfold_read_specification",
            "unfold_read_default_limit",
            "groupby_read_specification"
        );
        expect(kwargs.context.max_number_opened_groups).toBe(500);
        const result = super.web_read_group(...args);
        // Stand in for odoo/addons/web/models/models.py:819 and 833-887: replay
        // the server's one-level loop with the context limit, not the mock's 10.
        const maxOpenedGroups = kwargs.context.max_number_opened_groups || 10;
        const openingInfo = new Map(
            kwargs.opening_info?.map((info) => [info.value, info]) || []
        );
        const groupby = kwargs.groupby[0];
        const groupbyField = this._fields[groupby.split(":")[0]];
        const relatedModel = this.env[groupbyField.relation];
        const foldField = relatedModel?._fold_name;
        const hasFoldField = foldField in relatedModel._fields;
        let openedGroups = result.groups.filter((group) => group.__records).length;
        for (const group of result.groups) {
            const value = Array.isArray(group[groupby]) ? group[groupby][0] : group[groupby];
            const info = openingInfo.get(value);
            let limit = kwargs.unfold_read_default_limit;
            let offset = 0;
            let extraDomain = [];
            if (info) {
                if (info.folded) {
                    continue;
                }
                limit = info.limit;
                offset = info.offset;
                extraDomain = info.progressbar_domain || [];
            } else if (
                !kwargs.auto_unfold && !hasFoldField
                || openedGroups >= maxOpenedGroups
                || hasFoldField && group[foldField]
                || groupbyField.relation && !group[groupby]
            ) {
                continue;
            }
            openedGroups++;
            if (offset && offset >= group.__count) {
                offset = 0;
                group.__offset = 0;
            }
            group.__records = this.web_search_read(
                [...group.__extra_domain, ...kwargs.domain, ...extraDomain],
                kwargs.unfold_read_specification,
                offset,
                limit,
                kwargs.order
            ).records;
        }
        return result;
    }
}

defineMailModels();
defineModels([Picking, Move]);

test("All the groups are unfolded and keep the user choice", async () => {
    await mountView({
        type: "kanban",
        resModel: "move",
        arch: `
            <kanban js_class="base_weight_record_kanban">
                <templates>
                    <t t-name="card">
                        <field name="picking_id"/>
                    </t>
                </templates>
            </kanban>`,
        groupBy: ["picking_id"],
    });
    // Core would only open the first 10 groups
    expect(".o_kanban_group").toHaveCount(12);
    expect(".o_column_folded").toHaveCount(0);
    expect(".o_kanban_record").toHaveCount(12);
    await contains("[data-icon='folder_open']", {root: getKanbanColumn(0)}).click();
    expect(getKanbanColumn(0)).toHaveClass("o_column_folded");
    // Reload the view as it happens after each weighing
    await click(".o_searchview_input");
    await press("Enter");
    await animationFrame();
    expect(getKanbanColumn(0)).toHaveClass("o_column_folded");
    expect(".o_column_folded").toHaveCount(1);
    expect(".o_kanban_record").toHaveCount(11);
});
