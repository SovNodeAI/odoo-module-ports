/* Copyright 2026 SovNode AI
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import { animationFrame, expect, getFixture, test } from "@odoo/hoot";
import { View } from "@web/views/view";
import {
    contains,
    defineModels,
    defineWebModels,
    fields,
    models,
    mountWithCleanup,
    onRpc,
    parseViewProps,
} from "@web/../tests/web_test_helpers";

/**
 * The DF-e banner is mounted by the ``dfe_document_list`` list view, which is
 * the only way it reaches the screen. Mounting the view (instead of the
 * component alone) is what proves the view template, the component props and
 * the banner template all work together on the current Owl version.
 */
class DfeDocument extends models.Model {
    _name = "l10n_br_fiscal_dfe.document";

    name = fields.Char();

    _records = [{ id: 1, name: "document" }];
}

defineModels([DfeDocument]);
defineWebModels();

// The web client starts the mail store (mail is installed through queue_job);
// it is not what this module tests, so answer its fetch with an empty payload.
onRpc("/mail/store", () => ({}));

const bannerData = {
    fiscal_type: "nfe",
    last_query: "2026-01-01 10:00:00",
    next_query: "2026-01-01 11:00:00",
    last_status: "Documents found",
    last_status_code: "138",
    last_nsu: "10",
    max_nsu: "10",
    nsu_synced: true,
    auto_fetch: true,
    is_homologation: false,
    today_count: 3,
    pending_import_count: 1,
    never_queried: false,
    inactivity_days: 1,
    inactivity_warning: false,
    nsu_action_id: null,
    log_action_id: null,
};

/**
 * Mount the list view the way the action manager does, but without the main
 * components container (its mail chat hub needs models this module does not
 * use).
 *
 * @param {object} params
 */
async function mountDfeListView(params) {
    const actionManagerEl = document.createElement("div");
    actionManagerEl.classList.add("o_action_manager");
    getFixture().appendChild(actionManagerEl);
    return mountWithCleanup(View, {
        componentEnv: { config: params.config },
        props: parseViewProps(params),
        target: actionManagerEl,
        noMainContainer: true,
    });
}

test("the list view renders the DF-e banner above the records", async () => {
    const calls = [];
    onRpc("res.company", "dfe_get_banner_data", ({ args }) => {
        calls.push(args[0]);
        return bannerData;
    });

    await mountDfeListView({
        resModel: "l10n_br_fiscal_dfe.document",
        type: "list",
        arch: `<list js_class="dfe_document_list"><field name="name"/></list>`,
        context: { default_fiscal_type: "nfe" },
    });

    expect(".o_dfe_banner").toHaveCount(1);
    expect(".o_dfe_banner_search_all").toHaveCount(1);
    expect(".o_dfe_banner_specific_search").toHaveCount(1);
    expect(".o_dfe_banner").toHaveText(/Documents Today/);
    expect(".o_dfe_banner").toHaveText(/Last Query/);
    expect(".o_data_row").toHaveCount(1);
    expect(calls.length).toBeGreaterThan(0);
    expect(calls.every((fiscalType) => fiscalType === "nfe")).toBe(true);
});

test("the banner buttons call the company actions and reload the banner", async () => {
    const calls = [];
    onRpc("res.company", "dfe_get_banner_data", () => {
        calls.push("banner data");
        return bannerData;
    });
    onRpc("res.company", "dfe_action_search_all", ({ args }) => {
        calls.push(`search all ${args[0]}`);
        // A falsy action makes the banner reload its data.
        return false;
    });

    await mountDfeListView({
        resModel: "l10n_br_fiscal_dfe.document",
        type: "list",
        arch: `<list js_class="dfe_document_list"><field name="name"/></list>`,
        context: { default_fiscal_type: "nfe" },
    });

    calls.length = 0;
    await contains(".o_dfe_banner_search_all").click();
    await animationFrame();

    expect(calls).toEqual(["search all nfe", "banner data"]);
});
