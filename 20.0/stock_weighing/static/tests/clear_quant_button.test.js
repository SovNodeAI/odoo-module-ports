/* Copyright 2026 SovNode AI
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import {describe, expect, test} from "@odoo/hoot";
import {defineMailModels} from "@mail/../tests/mail_test_helpers";
import {
    contains,
    defineModels,
    fields,
    models,
    mountView,
    patchWithCleanup,
} from "@web/../tests/web_test_helpers";
import {Record} from "@web/model/relational_model/record";

// Keep this test explicit instead of adding its views to TestStockWeighingJs's
// single-test filter: both tests still run in web.assets_unit_tests.
describe.current.tags("desktop");

class Quant extends models.Model {
    name = fields.Char();

    _records = [{id: 1, name: "Source stock"}];
}

class Lot extends models.Model {
    name = fields.Char();

    _records = [{id: 1, name: "Lot 001"}];
}

class WeighingWizard extends models.Model {
    _name = "weighing.wizard";

    quant_id = fields.Many2one({relation: "quant"});
    lot_id = fields.Many2one({relation: "lot"});

    _records = [{id: 1, quant_id: 1, lot_id: 1}];
}

class OtherModel extends models.Model {
    quant_id = fields.Many2one({relation: "quant"});

    _records = [{id: 1, quant_id: 1}];
}

defineMailModels();
defineModels([Quant, Lot, WeighingWizard, OtherModel]);

test("Clear quant button clears quant and lot in the weighing wizard", async () => {
    patchWithCleanup(Record.prototype, {
        update(changes) {
            if (this.resModel === "weighing.wizard") {
                expect(changes).toEqual({quant_id: false, lot_id: false});
                expect.step("record.update");
            }
            return super.update(changes);
        },
    });
    await mountView({
        type: "form",
        resModel: "weighing.wizard",
        resId: 1,
        arch: `<form>
            <field name="quant_id"/>
            <field name="lot_id"/>
        </form>`,
    });
    expect(".o_weighing_clear_quant_btn").toHaveCount(1);
    await contains(".o_weighing_clear_quant_btn").click();
    await expect.waitForSteps(["record.update"]);
    expect(".o_field_many2one[name='quant_id'] input").toHaveValue("");
    expect(".o_field_many2one[name='lot_id'] input").toHaveValue("");
    expect(".o_weighing_clear_quant_btn").toHaveCount(0);
});

test("Clear quant button is absent from an ordinary many2one field", async () => {
    await mountView({
        type: "form",
        resModel: "other.model",
        resId: 1,
        arch: `<form><field name="quant_id"/></form>`,
    });
    expect(".o_field_many2one[name='quant_id'] input").toHaveValue("Source stock");
    expect(".o_weighing_clear_quant_btn").toHaveCount(0);
});
