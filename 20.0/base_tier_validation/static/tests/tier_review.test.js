/* Copyright 2026 SovNode AI
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import {defineMailModels} from "@mail/../tests/mail_test_helpers";
import {expect, test} from "@odoo/hoot";
import {click, queryAllTexts, queryOne} from "@odoo/hoot-dom";
import {
    defineModels,
    fields,
    mockService,
    models,
    mountView,
    mountWithCleanup,
    serverState,
} from "@web/../tests/web_test_helpers";

import {TierReviewMenu} from "@base_tier_validation/components/tier_review_menu/tier_review_menu.esm";

class TierReview extends models.Model {
    _name = "tier.review";

    name = fields.Char();
    sequence = fields.Integer();
    display_status = fields.Char();
    todo_by = fields.Char();
    status = fields.Char();
    reviewed_formated_date = fields.Char();
    comment = fields.Char();
    requested_by = fields.Many2one({relation: "res.users"});
    done_by = fields.Many2one({relation: "res.users"});
    res_id = fields.Integer();

    _records = [
        {
            id: 1,
            name: "Tier 1",
            sequence: 1,
            display_status: "Approved",
            todo_by: "",
            status: "approved",
            reviewed_formated_date: "01/01/2026",
            comment: "ok",
            requested_by: serverState.userId,
            done_by: serverState.userId,
            res_id: 1,
        },
        {
            id: 2,
            name: "Tier 2",
            sequence: 2,
            display_status: "Pending",
            todo_by: "Admin",
            status: "pending",
            reviewed_formated_date: "",
            comment: "",
            requested_by: serverState.userId,
            done_by: false,
            res_id: 1,
        },
    ];
}

class TierValidationTester extends models.Model {
    _name = "tier.validation.tester";

    name = fields.Char();
    review_ids = fields.One2many({
        relation: "tier.review",
        relation_field: "res_id",
    });

    _records = [{id: 1, name: "Tester", review_ids: [1, 2]}];
}

defineMailModels();
defineModels([TierReview, TierValidationTester]);

test("tier validation widget renders the reviews of the record", async () => {
    await mountView({
        type: "form",
        resModel: "tier.validation.tester",
        resId: 1,
        arch: `<form><field name="review_ids" widget="tier_validation"/></form>`,
    });
    expect(".o_review table tbody tr").toHaveCount(2);
    expect(queryAllTexts(".o_review tbody tr td[name='td_name']")).toEqual([
        "Tier 1",
        "Tier 2",
    ]);
    expect(queryAllTexts(".o_review tbody tr td[name='td_display_status']")).toEqual([
        "Approved",
        "Pending",
    ]);
});

test("tier validation widget toggles the reviews panel", async () => {
    await mountView({
        type: "form",
        resModel: "tier.validation.tester",
        resId: 1,
        arch: `<form><field name="review_ids" widget="tier_validation"/></form>`,
    });
    const panel = queryOne("#collapse1");
    expect(panel.style.display).toBe("");
    await click(".o_info_btn");
    expect(panel.style.display).toBe("block");
    await click(".o_info_btn");
    expect(panel.style.display).toBe("none");
});

test("tier review systray menu shows the pending reviews count", async () => {
    mockService("orm", () => ({
        async call(model, method) {
            expect.step(`${model}.${method}`);
            return [
                {
                    model: "res.partner",
                    name: "Partner",
                    pending_count: 2,
                    icon: "/base/static/description/icon.png",
                },
                {
                    model: "res.users",
                    name: "User",
                    pending_count: 1,
                    icon: "/base/static/description/icon.png",
                },
            ];
        },
    }));
    await mountWithCleanup(TierReviewMenu);
    expect(".o-mail-ActivityMenu-counter").toHaveText("3");
    expect.verifySteps(["res.users.review_user_count"]);
});
