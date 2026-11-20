import { describe, expect, test } from "@odoo/hoot";
import { click, queryFirst } from "@odoo/hoot-dom";
import { defineModels, fields, models, mountView } from "@web/../tests/web_test_helpers";

class User extends models.Model {
    _name = "res.users";

    has_group() {
        return true;
    }
}

class Partner extends models.Model {
    name = fields.Char();

    _records = [
        { id: 1, name: "First" },
        { id: 2, name: "Second" },
    ];
}

defineModels([Partner, User]);

describe.current.tags("desktop");

test("open_tab widget renders a link to the record in a new tab", async () => {
    await mountView({
        resModel: "partner",
        type: "list",
        arch: `
            <list>
                <field name="id" widget="open_tab" nolabel="1"/>
                <field name="name"/>
            </list>`,
    });

    expect(".o_data_row .open_tab_widget").toHaveCount(2);
    expect(".o_data_row:first .open_tab_widget").toHaveAttribute("href", "/odoo/partner/1");
    expect(".o_data_row:last .open_tab_widget").toHaveAttribute("href", "/odoo/partner/2");
    expect(".o_data_row:first .open_tab_widget").toHaveAttribute("target", "_blank");
    expect(".o_data_row:first .open_tab_widget").toHaveAttribute(
        "title",
        "Click to open on new tab"
    );
});

test("clicking the open_tab link does not open the record in the current view", async () => {
    await mountView({
        resModel: "partner",
        type: "list",
        arch: `
            <list>
                <field name="id" widget="open_tab" nolabel="1"/>
                <field name="name"/>
            </list>`,
    });

    let rowClicked = false;
    queryFirst(".o_data_row").addEventListener("click", () => {
        rowClicked = true;
    });

    await click(".o_data_row:first .open_tab_widget");

    // The widget stops the click, so the list cell handler never opens the record.
    expect(rowClicked).toBe(false);
    expect(".o_form_renderer").toHaveCount(0);
});
