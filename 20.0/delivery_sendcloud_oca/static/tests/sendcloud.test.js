/* Copyright 2026 SovNode AI
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

import {expect, test} from "@odoo/hoot";
import {animationFrame} from "@odoo/hoot-mock";
import {queryAllTexts} from "@odoo/hoot-dom";
import {
    contains,
    defineModels,
    fields,
    mockService,
    models,
    mountView,
    onRpc,
    patchWithCleanup,
} from "@web/../tests/web_test_helpers";
import {defineMailModels} from "@mail/../tests/mail_test_helpers";
import {assets} from "@web/core/assets";

class SendcloudTest extends models.Model {
    _name = "sendcloud.test";

    sendcloud_service_point_address = fields.Text();
    sendcloud_sp_details = fields.Char();

    _records = [
        {
            id: 1,
            sendcloud_service_point_address: JSON.stringify({
                name: "Service Point Amsterdam",
                street: "Damrak",
                house_number: "1",
                postal_code: "1012LG",
                city: "Amsterdam",
            }),
            sendcloud_sp_details: JSON.stringify({
                api_key: "key",
                country: "nl",
                postalcode: "1012LG",
                language: "en-us",
                carrier: "postnl",
            }),
        },
    ];
}

defineModels([SendcloudTest]);
defineMailModels();

const servicePointArch = `
    <form>
        <field name="sendcloud_service_point_address"
               widget="sendcloud_service_point_selector"/>
    </form>`;

const onboardingSteps = [
    {
        id: 1,
        title: "Setup Integration",
        description: "Setup Sendcloud Integration.",
        state: "not_done",
        action: "action_open_sendcloud_onboarding_integration",
        done_icon: "star",
        button_text: "Setup",
        done_text: "Well done!",
        step_image_alt: "Setup Integration",
    },
    {
        id: 2,
        title: "Sync Sendcloud objects",
        description: "Synchronize Sendcloud objects.",
        state: "not_done",
        action: "action_sendcloud_onboarding_sync",
        done_icon: "star",
        button_text: "Sync",
        done_text: "Looks great!",
        step_image_alt: "Sync Sendcloud objects",
    },
];

test("service point selector field renders the selected service point", async () => {
    // The widget loads the Sendcloud library on start; the library itself is not
    // needed to render the selected service point.
    patchWithCleanup(assets, {
        loadJS: () => Promise.resolve(),
    });

    await mountView({
        type: "form",
        resModel: "sendcloud.test",
        resId: 1,
        arch: servicePointArch,
    });

    expect(".o_delivery_sendcloud_widget").toHaveCount(1);
    expect(queryAllTexts(".o_delivery_sendcloud_detail > div")).toEqual([
        "Service Point Amsterdam",
        "Damrak1",
        "1012LG",
        "Amsterdam",
    ]);
    expect(".o_delivery_sendcloud_select").toHaveCount(1);
    expect(".o_delivery_sendcloud_clear").toHaveCount(1);
});

test("service point selector field clears the service point", async () => {
    patchWithCleanup(assets, {
        loadJS: () => Promise.resolve(),
    });

    await mountView({
        type: "form",
        resModel: "sendcloud.test",
        resId: 1,
        arch: servicePointArch,
    });

    expect(".o_delivery_sendcloud_clear").toHaveCount(1);
    await contains(".o_delivery_sendcloud_clear").click();
    await animationFrame();
    expect(".o_delivery_sendcloud_clear").toHaveCount(0);
    expect(".o_delivery_sendcloud_detail").toHaveText("");
});

test("sendcloud list renderer displays the onboarding panel", async () => {
    onRpc("onboarding.onboarding", "get_sendcloud_onboarding_data", () => ({
        onboarding_state: "not_done",
        steps: onboardingSteps,
    }));

    await mountView({
        type: "list",
        resModel: "sendcloud.test",
        arch: `
            <list js_class="sendcloud_list">
                <field name="sendcloud_service_point_address"/>
            </list>`,
    });

    expect(".o_onboarding_main").toHaveCount(1);
    expect(".o_onboarding_step").toHaveCount(2);
    expect(queryAllTexts(".o_onboarding_step_title")).toEqual([
        "Setup Integration",
        "Sync Sendcloud objects",
    ]);
    expect(".o_onboarding_step_action").toHaveCount(2);
});

test("clicking an onboarding step opens its action", async () => {
    const actions = [];
    mockService("action", {
        doAction(action, options) {
            actions.push({action, options});
        },
    });
    onRpc("onboarding.onboarding", "get_sendcloud_onboarding_data", () => ({
        onboarding_state: "not_done",
        steps: onboardingSteps,
    }));
    onRpc("onboarding.onboarding.step", "action_open_sendcloud_onboarding_integration", () => ({
        type: "ir.actions.act_window",
        res_model: "sendcloud.integration.wizard",
    }));

    await mountView({
        type: "list",
        resModel: "sendcloud.test",
        arch: `
            <list js_class="sendcloud_list">
                <field name="sendcloud_service_point_address"/>
            </list>`,
    });

    await contains(".o_onboarding_step_action").click();
    expect(actions).toHaveLength(1);
    expect(actions[0].action.res_model).toBe("sendcloud.integration.wizard");
    expect(typeof actions[0].options.onClose).toBe("function");
});
