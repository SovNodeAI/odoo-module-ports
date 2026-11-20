/* Copyright 2026 SovNode AI
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import { expect, test } from "@odoo/hoot";
import { waitFor } from "@odoo/hoot-dom";
import { mailModels } from "@mail/../tests/mail_test_helpers";
import {
    contains,
    defineModels,
    fields,
    models,
    mountView,
    onRpc,
} from "@web/../tests/web_test_helpers";
import "@mis_builder/components/mis_report_widget.esm";

class MisReportInstance extends models.Model {
    _name = "mis.report.instance";

    source_aml_model_name = fields.Char();
    widget_show_filters = fields.Boolean();
    widget_show_settings_button = fields.Boolean();
    widget_search_view_id = fields.Integer();
    pivot_date = fields.Date();
    widget_show_pivot_date = fields.Boolean();
    wide_display_by_default = fields.Boolean();
    user_can_read_annotation = fields.Boolean();
    user_can_edit_annotation = fields.Boolean();

    _records = [
        {
            id: 1,
            source_aml_model_name: "account.move.line",
            widget_show_filters: false,
            widget_show_settings_button: false,
            widget_search_view_id: false,
            pivot_date: false,
            widget_show_pivot_date: false,
            wide_display_by_default: false,
            user_can_read_annotation: true,
            user_can_edit_annotation: true,
        },
    ];
}

class MisReportInstanceAnnotation extends models.Model {
    _name = "mis.report.instance.annotation";

    set_annotation(cellId, instanceId, text) {
        expect.step(`save annotation: ${cellId} ${instanceId} ${text}`);
        return true;
    }
}

defineModels({ ...mailModels, MisReportInstance, MisReportInstanceAnnotation });

test("MIS report widget renders and saves an annotation", async () => {
    onRpc("mis.report.instance", "read", ({ args }) => [
        {
            id: args[0][0],
            source_aml_model_name: false,
            widget_show_filters: false,
            widget_show_settings_button: false,
            widget_search_view_id: false,
            pivot_date: false,
            widget_show_pivot_date: false,
            wide_display_by_default: false,
            user_can_read_annotation: true,
            user_can_edit_annotation: true,
        },
    ]);
    onRpc("mis.report.instance", "compute", () => ({
        header: [{ cols: [{ label: "Account", colspan: 1 }] }],
        body: [
            {
                label: "Income",
                style: false,
                cells: [
                    {
                        val_r: "100.00",
                        val_c: "100.00",
                        style: false,
                        cell_id: "cell-1",
                        can_be_annotated: true,
                        drilldown_arg: false,
                    },
                ],
            },
        ],
        notes: {},
    }));
    onRpc("mis.report.instance", "get_notes_by_cell_id", () => ({
        "cell-1": { sequence: 1, text: "Updated note" },
    }));

    await mountView({
        resModel: "mis.report.instance",
        resId: 1,
        type: "form",
        arch: `<form><sheet><field name="id" widget="mis_report_widget"/></sheet></form>`,
    });
    expect(".oe_mis_builder_content").toHaveCount(1);
    expect(".mis_builder_amount").toHaveText("100.00");
    expect("#icon_resize").toHaveAttribute("data-icon", "expand_content");
    expect(".o_form_sheet_bg").not.toHaveClass("oe_mis_builder_report_wide_sheet");
    await contains("#icon_resize").click({ focus: false });
    expect("#icon_resize").toHaveAttribute("data-icon", "close_fullscreen");
    expect(".o_form_sheet_bg").toHaveClass("oe_mis_builder_report_wide_sheet");

    await contains(".oe_mis_builder_dropdown .dropdown-toggle").click({ focus: false });
    await contains(".oe_mis_builder_dropdown .js_tag").click({ focus: false });
    expect(".modal textarea").toHaveValue("");
    await contains(".modal textarea").edit("Updated note", { focus: false });
    await contains(".modal-footer .btn-primary").click({ focus: false });
    await waitFor(".oe_mis_builder_footnote_table:contains(Updated note)");
    expect(".oe_mis_builder_footnote_table").toHaveText("1. Updated note");
    expect.verifySteps(["save annotation: cell-1 1 Updated note"]);
});
