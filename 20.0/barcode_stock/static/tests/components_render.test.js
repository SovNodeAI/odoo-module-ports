import {beforeEach, describe, expect, test} from "@odoo/hoot";
import {queryAll, queryFirst} from "@odoo/hoot-dom";
import {defineMailModels} from "@mail/../tests/mail_test_helpers";
import {mountWithCleanup, mockService} from "@web/../tests/web_test_helpers";
import {PickingDoneCard} from "@barcode_stock/js/components/picking_done_card.esm";
import {PickingDoneList} from "@barcode_stock/js/components/picking_done_list.esm";
import {PickingInfoTab} from "@barcode_stock/js/components/picking_info_tab.esm";
import {PickingMoveCard} from "@barcode_stock/js/components/picking_move_card.esm";
import {PickingMoveList} from "@barcode_stock/js/components/picking_move_list.esm";

/**
 * The module's components, mounted the way Odoo mounts a component: their
 * templates are compiled and rendered by Owl, so a template that still speaks
 * Owl 2 (a bare `state`, a `t-model` without `.proxy`, a `t-esc`) fails here
 * instead of only in the browser.
 */
// The web client starts the mail store, which reads its models from the mock
// server: define them as Odoo's own stock tests do.
defineMailModels();

describe("BarcodeStock", () => {
    beforeEach(() => {
        // The barcode app's scan service is not what these components render;
        // starting it would only pull the whole barcode app in.
        mockService("barcodeScannerBarcode", () => ({}));
    });

    test("a move card renders the move it is given", async () => {
        await mountWithCleanup(PickingMoveCard, {
            noMainContainer: true,
            props: {
                move: {id: 5, product_id: [7, "Duck confit"], quantity: 4},
                moveLines: [],
                stats: {demandQty: 4, doneQty: 1, remainingQty: 3, completionLabel: "25%"},
                onClick: () => {},
            },
        });
        expect(queryFirst(".ilx-picking-move-card")).toHaveText(/Duck confit/);
        expect(queryFirst(".ilx-kw-group-badge")).toHaveText("25%");
    });

    test("a move list renders the moves still to pick", async () => {
        await mountWithCleanup(PickingMoveList, {
            noMainContainer: true,
            props: {
                moves: [
                    {id: 5, product_id: [7, "Duck confit"], quantity: 4, qty_done_total: 0},
                    {id: 6, product_id: [8, "Ham"], quantity: 2, qty_done_total: 2},
                ],
                moveLines: [],
                moveStatsById: {},
                onOpenWizard: () => {},
            },
        });
        // The completed move is left out of the To Do list.
        expect(queryAll(".ilx-picking-move-card")).toHaveCount(1);
        expect(queryFirst(".ilx-picking-move-card")).toHaveText(/Duck confit/);
    });

    test("a done card renders the line it is given", async () => {
        await mountWithCleanup(PickingDoneCard, {
            noMainContainer: true,
            props: {
                line: {id: 1, product_id: [7, "Duck confit"], move_id: [5, "Move"], qty_picked: 2},
                onDelete: () => {},
            },
        });
        expect(queryFirst(".ilx-picking-done-card")).toHaveText(/Duck confit/);
    });

    test("a done list renders the lines that were picked", async () => {
        await mountWithCleanup(PickingDoneList, {
            noMainContainer: true,
            props: {
                lines: [
                    {id: 1, product_id: [7, "Duck confit"], move_id: [5, "Move"], qty_picked: 2},
                    {id: 2, product_id: [8, "Ham"], move_id: [6, "Move"], qty_picked: 0},
                ],
                onDeleteLine: () => {},
            },
        });
        expect(queryAll(".ilx-picking-done-card")).toHaveCount(1);
    });

    test("an info tab renders the picking it is given", async () => {
        await mountWithCleanup(PickingInfoTab, {
            noMainContainer: true,
            props: {
                picking: {
                    id: 3,
                    partner_id: [11, "Azure Interior"],
                    location_id: [8, "WH/Stock"],
                    location_dest_id: [9, "Customers"],
                    user_id: false,
                    scheduled_date: "2026-11-18 12:00:00",
                    note: "<p>pick 5 &lt; 10</p>",
                },
                onSelectResponsible: () => {},
            },
        });
        expect(queryFirst(".ilx-kw-title")).toHaveText("Azure Interior");
        expect(queryFirst("textarea")).toHaveValue("pick 5 < 10");
    });
});
