import {animationFrame, click, expect, test} from "@odoo/hoot";
import {
    defineModels,
    fields,
    findComponent,
    mockService,
    models,
    mountView,
    onRpc,
} from "@web/../tests/web_test_helpers";
import {defineMailModels} from "@mail/../tests/mail_test_helpers";
import {queryAllTexts} from "@odoo/hoot-dom";

class MainElement extends models.Model {
    _name = "main.element";

    name = fields.Char({readonly: false});
    is_reconciled = fields.Boolean();
    to_check = fields.Boolean();
    aggregate_id = fields.Integer();
    reconcile_aggregate = fields.Selection({selection: []});

    _views = {
        kanban: `
            <kanban js_class="reconcile">
                <templates>
                    <t t-name="card">
                        <div class="o_kanban_record_title" t-att-data-id="record.name.raw_value"><field name="name"/></div>
                    </t>
                </templates>
            </kanban>
        `,
        form: `
            <form js_class="reconcile_form">
                <header>
                    <button name="reconcile_bank_line" string="Reconcile" type="object"/>
                </header>
                <group><field name="name"/></group>
                <field name="is_reconciled" invisible="1"/>
            </form>
        `,
    };
    _records = [
        {id: 1, name: "value 1", is_reconciled: true},
        {id: 2, name: "value 2"},
    ];
}

defineModels([MainElement]);
// As we use mail as a dependancy, we need to declare models.
defineMailModels();

test("Check Kanban View", async () => {
    await mountView({
        type: "kanban",
        resIds: [1, 2],
        resModel: "main.element",
    });
    expect(".o_kanban_record .o_kanban_record_title").toHaveCount(2);
    expect(queryAllTexts(".o_kanban_record .o_kanban_record_title")).toEqual([
        "value 1",
        "value 2",
    ]);
    expect(".o_account_reconcile_oca_info .o_form_view").toHaveCount(0);
    await click(".o_kanban_record .o_kanban_record_title");
    await animationFrame();
    expect(".o_account_reconcile_oca_info .o_form_view").toHaveCount(1);
    expect(
        queryAllTexts(
            ".o_kanban_record.o_kanban_record_reconcile_oca_selected .o_kanban_record_title"
        )
    ).toEqual(["value 1"]);
    await animationFrame();
    expect(
        ".o_account_reconcile_oca_info .o_form_view .o_field_widget[name='name'] input"
    ).toHaveValue("value 1");
    await click(".o_kanban_record .o_kanban_record_title[data-id='value 2']");
    await animationFrame();
    expect(
        queryAllTexts(
            ".o_kanban_record.o_kanban_record_reconcile_oca_selected .o_kanban_record_title"
        )
    ).toEqual(["value 2"]);
    await animationFrame();
    expect(
        ".o_account_reconcile_oca_info .o_form_view .o_field_widget[name='name'] input"
    ).toHaveValue("value 2");
});

test("Switching from a dirty reconcile form saves and refreshes the cards", async () => {
    const view = await mountView({
        type: "kanban",
        resIds: [1, 2],
        resModel: "main.element",
    });
    await click(".o_kanban_record .o_kanban_record_title");
    await animationFrame();
    expect(".o_form_view .o_field_widget[name='name'] input").toHaveValue("value 1");
    const parent = findComponent(view, (component) => component.form_controller);
    const form = parent.form_controller;
    await form.model.root.switchMode("edit");
    form.model.root.data.is_reconciled = true;
    await animationFrame();
    expect(".o_form_view input:not([readonly])").toHaveValue("value 1");
    await form.model.root.update({name: "updated value 1"});
    await animationFrame();
    expect(".o_form_dirty").toHaveCount(1);
    await click(".o_kanban_record .o_kanban_record_title[data-id='value 2']");
    await animationFrame();
    expect(".o_form_view .o_field_widget[name='name'] input").toHaveValue("value 2");
});

test("Closing the create line dialog refreshes the reconciliation view", async () => {
    onRpc("main.element", "action_new_line", () => {
        expect.step("create line");
        return {type: "ir.actions.act_window_close"};
    });
    mockService("action", {
        doAction(action, options) {
            expect.step("open create line");
            return options.onClose();
        },
    });
    await mountView({
        type: "kanban",
        resIds: [1, 2],
        resModel: "main.element",
    });
    expect(".o_kanban_record .o_kanban_record_title").toHaveCount(2);
    await click(".o_control_panel_main_buttons button");
    await animationFrame();
    expect.verifySteps(["create line", "open create line"]);
    expect(".o_kanban_record .o_kanban_record_title").toHaveCount(2);
});
