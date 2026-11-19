/* Copyright 2026 SovNode AI
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import { expect, test } from "@odoo/hoot";
import { defineMailModels } from "@mail/../tests/mail_test_helpers";
import { defineModels, fields, models, mountView } from "@web/../tests/web_test_helpers";

class Stay extends models.Model {
    _name = "stay.stay";

    name = fields.Char();
    guest_qty = fields.Integer();

    _records = [{ id: 1, name: "Stay 1", guest_qty: 2 }];

    // Stands for stay.stay.get_dashboard_data (addons/stay/models/stay.py:924):
    // the real server aggregates stay.line and stay.stay rows for today and tomorrow.
    get_dashboard_data() {
        return {
            today_breakfast: 3,
            today_lunch: 4,
            today_dinner: 5,
            today_night: 6,
            today_arrival: 7,
            today_departure: 8,
            tomorrow_breakfast: 9,
            tomorrow_lunch: 10,
            tomorrow_dinner: 11,
            tomorrow_night: 12,
            tomorrow_arrival: 13,
            tomorrow_departure: 14,
        };
    }

    _views = {
        "list,false": `<list js_class="stay_dashboard_list"><field name="name"/></list>`,
        "search,false": `<search/>`,
    };
}

defineModels([Stay]);
defineMailModels();

test("stay dashboard list renders the KPI values of get_dashboard_data", async () => {
    await mountView({
        resModel: "stay.stay",
        type: "list",
        arch: `<list js_class="stay_dashboard_list"><field name="name"/></list>`,
        searchViewId: false,
        searchViewArch: `<search/>`,
    });

    expect("#today_breakfast .fs-2").toHaveText("3");
    expect("#today_lunch .fs-2").toHaveText("4");
    expect("#today_dinner .fs-2").toHaveText("5");
    expect("#today_night .fs-2").toHaveText("6");
    expect("#today_arrival .fs-2").toHaveText("7");
    expect("#today_departure .fs-2").toHaveText("8");
    expect("#tomorrow_breakfast .w-100").toHaveText("9");
    expect("#tomorrow_lunch .w-100").toHaveText("10");
    expect("#tomorrow_dinner .w-100").toHaveText("11");
    expect("#tomorrow_night .w-100").toHaveText("12");
    expect("#tomorrow_arrival .w-100").toHaveText("13");
    expect("#tomorrow_departure .w-100").toHaveText("14");
});
