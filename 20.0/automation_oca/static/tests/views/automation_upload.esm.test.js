import { click } from "@odoo/hoot-dom";
import { animationFrame } from "@odoo/hoot-mock";
import { Component, xml } from "@odoo/owl";
import { expect, test } from "@odoo/hoot";
import {
    defineModels,
    fields,
    models,
    mountView,
    mountWithCleanup,
    registerTemplate,
} from "@web/../tests/web_test_helpers";
import { defineMailModels } from "@mail/../tests/mail_test_helpers";
import { AutomationFileUploader } from "@automation_oca/views/automation_upload/automation_upload.esm";

class Configuration extends models.Model {
    name = fields.Char();
    state = fields.Selection({ selection: [["draft", "Draft"]] });
    step_ids = fields.One2many({
        relation: "configuration.step",
        relation_field: "configuration_id",
    });

    _records = [{ id: 1, name: "Automation", state: "draft", step_ids: [1, 2] }];
}

class ConfigurationStep extends models.Model {
    _name = "configuration.step";

    name = fields.Char();
    configuration_id = fields.Many2one({ relation: "configuration" });
    parent_id = fields.Many2one({ relation: "configuration.step" });
    trigger_child_types = fields.Json();

    _records = [
        {
            id: 1,
            name: "Step 1",
            configuration_id: 1,
            trigger_child_types: {
                after_step: {
                    name: "After step",
                    icon: "fork_right",
                    color: "text-success",
                },
            },
        },
        {
            id: 2,
            name: "Step 2",
            configuration_id: 1,
            parent_id: 1,
            trigger_child_types: {},
        },
    ];
}

defineModels([Configuration, ConfigurationStep]);
defineMailModels();

const workflowArch = `
    <field name="step_ids" widget="automation_step" mode="kanban">
        <kanban>
            <field name="id"/>
            <field name="parent_id"/>
            <field name="trigger_child_types"/>
            <templates>
                <div t-name="card">
                    <a class="o_open_step" type="open"><field name="name"/></a>
                    <a class="o_edit_step" t-if="widget.editable" type="open">Edit</a>
                    <a class="o_delete_step" t-if="widget.deletable" type="delete">Delete</a>
                    <div class="o_child_buttons" t-if="widget.editable">
                        <t t-foreach="record.trigger_child_types.raw_value" t-as="trigger_type_id" t-key="trigger_type_id">
                            <t t-set="trigger" t-value="record.trigger_child_types.raw_value[trigger_type_id]"/>
                            <i class="oi o_child_icon"
                                t-att-class="trigger.color"
                                t-att-data-icon="trigger.icon"/>
                        </t>
                    </div>
                </div>
            </templates>
        </kanban>
        <form><field name="name"/></form>
    </field>
`;

test("Automation kanban renders its upload button", async () => {
    await mountView({
        type: "kanban",
        resModel: "configuration",
        arch: `<kanban js_class="automation_upload_kanban">
            <field name="state" readonly="1"/>
            <templates>
                <t t-name="card"><field name="name"/></t>
            </templates>
        </kanban>`,
    });
    expect("article.o_kanban_record").toHaveCount(1);
    expect("button.o_button_upload_bill").toHaveText("Upload");
});

test("Automation uploader renders a custom toggler template", async () => {
    registerTemplate(
        "automation_oca_test.UploadToggler",
        `<button class="o_custom_upload">Custom upload</button>`
    );
    class Parent extends Component {
        static components = { AutomationFileUploader };
        static template = xml`
            <AutomationFileUploader togglerTemplate="'automation_oca_test.UploadToggler'">
                <t t-set-slot="toggler">
                    <button class="o_default_upload">Upload</button>
                </t>
            </AutomationFileUploader>
        `;
    }
    await mountWithCleanup(Parent);
    expect("button.o_custom_upload").toHaveText("Custom upload");
    expect("button.o_default_upload").toHaveCount(0);
});

test("Workflow card links open records and render icons", async () => {
    await mountView({
        type: "form",
        resId: 1,
        resModel: "configuration",
        arch: `<form>${workflowArch}</form>`,
    });
    expect("article.o_kanban_record:not(.o_kanban_ghost)").toHaveCount(2);
    expect(".o_child_icon").toHaveAttribute("data-icon", "fork_right");
    expect(".o_child_icon").toHaveClass("oi text-success");
    await click(".o_open_step:first");
    await animationFrame();
    expect(".o_dialog .o_form_view").toHaveCount(1);
});

test("Workflow card hides controls in readonly mode", async () => {
    await mountView({
        type: "form",
        resId: 1,
        resModel: "configuration",
        arch: `<form edit="0">${workflowArch}</form>`,
    });
    expect(".o_open_step").toHaveCount(2);
    expect(".o_edit_step").toHaveCount(0);
    expect(".o_delete_step").toHaveCount(0);
    expect(".o_child_buttons").toHaveCount(0);
});
