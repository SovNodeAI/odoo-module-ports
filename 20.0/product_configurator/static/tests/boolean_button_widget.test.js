/* Copyright 2026 SovNode AI
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import {expect, test} from "@odoo/hoot";
import {contains, defineModels, fields, models, mountView} from "@web/../tests/web_test_helpers";
import {defineMailModels} from "@mail/../tests/mail_test_helpers";

class ProductTemplate extends models.Model {
    _name = "product.template";

    config_ok = fields.Boolean({string: "Can be Configured"});

    _records = [
        {id: 1, config_ok: true},
        {id: 2, config_ok: false},
    ];
}

defineModels([ProductTemplate]);
defineMailModels();

const ARCH = `
    <form>
        <div class="oe_button_box" name="button_box">
            <button class="oe_stat_button" name="toggle_config" type="object" icon="build">
                <field
                    name="config_ok"
                    string="Configurable"
                    options="{'active': 'Configurable', 'inactive': 'Standard'}"
                    widget="boolean_button"
                />
            </button>
        </div>
    </form>
`;

async function checkLabels(resId, label, labelClass, hoverLabel, hoverClass) {
    await mountView({resModel: "product.template", resId, type: "form", arch: ARCH});

    expect(".o_boolean_button.o_not_hover").toHaveCount(1);
    expect(".o_boolean_button.o_not_hover").toHaveText(label);
    expect(".o_boolean_button.o_not_hover").toHaveClass(labelClass);
    expect(".o_boolean_button.o_hover").toHaveCount(1);
    expect(".o_boolean_button.o_hover").toHaveText(hoverLabel);
    expect(".o_boolean_button.o_hover").toHaveClass(hoverClass);
}

test.tags("desktop");
test("boolean_button field renders the active label in a form view", async () => {
    await checkLabels(1, "Configurable", "text-success", "Standard", "text-danger");
});

test.tags("desktop");
test("boolean_button field renders the inactive label in a form view", async () => {
    await checkLabels(2, "Standard", "text-danger", "Configurable", "text-success");
});

test.tags("mobile");
test("boolean_button field renders the active label in a form view (mobile)", async () => {
    await mountView({resModel: "product.template", resId: 1, type: "form", arch: ARCH});

    await contains(".o-form-buttonbox .o_button_more").click();
    expect(".o_boolean_button.o_not_hover").toHaveCount(1);
    expect(".o_boolean_button.o_not_hover").toHaveText("Configurable");
    expect(".o_boolean_button.o_not_hover").toHaveClass("text-success");
    expect(".o_boolean_button.o_hover").toHaveCount(1);
    expect(".o_boolean_button.o_hover").toHaveText("Standard");
    expect(".o_boolean_button.o_hover").toHaveClass("text-danger");
});

test.tags("mobile");
test("boolean_button field renders the inactive label in a form view (mobile)", async () => {
    await mountView({resModel: "product.template", resId: 2, type: "form", arch: ARCH});

    await contains(".o-form-buttonbox .o_button_more").click();
    expect(".o_boolean_button.o_not_hover").toHaveCount(1);
    expect(".o_boolean_button.o_not_hover").toHaveText("Standard");
    expect(".o_boolean_button.o_not_hover").toHaveClass("text-danger");
    expect(".o_boolean_button.o_hover").toHaveCount(1);
    expect(".o_boolean_button.o_hover").toHaveText("Configurable");
    expect(".o_boolean_button.o_hover").toHaveClass("text-success");
});
