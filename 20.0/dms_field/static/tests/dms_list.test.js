/* Copyright 2026 SovNode AI
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */
import {afterEach, expect, globals, test} from "@odoo/hoot";
import {waitFor} from "@odoo/hoot-dom";
import {
    contains,
    defineModels,
    fields,
    MockServer,
    models,
    mockService,
    mountView,
    onRpc,
    patchWithCleanup,
    serverState,
} from "@web/../tests/web_test_helpers";
import "@dms_field/views/fields/x2many/x2many_field.esm";
import {assets} from "@web/core/assets";
import {makeStore} from "@mail/model/export";
import {defineMailModels, mailModels} from "@mail/../tests/mail_test_helpers";
import {DmsListRenderer} from "@dms_field/views/dms_list/dms_list_renderer.esm";

class DmsStorage extends models.Model {
    _name = "dms.storage";
    name = fields.Char();
    count_storage_directories = fields.Integer();
    field_template_ids = fields.One2many({
        relation: "dms.field.template",
        relation_field: "storage_id",
    });
    _records = [
        {
            id: 1,
            name: "Partner documents",
            count_storage_directories: 1,
            field_template_ids: [1],
        },
    ];
}

class DmsFieldTemplate extends models.Model {
    _name = "dms.field.template";
    model = fields.Char();
    storage_id = fields.Many2one({relation: "dms.storage"});
    _records = [{id: 1, model: "res.partner", storage_id: 1}];
}

class DmsDirectory extends models.Model {
    _name = "dms.directory";
    name = fields.Char();
    storage_id = fields.Many2one({relation: "dms.storage"});
    res_model = fields.Char();
    res_id = fields.Integer();
    parent_id = fields.Many2one({relation: "dms.directory"});
    count_directories = fields.Integer();
    count_files = fields.Integer();
    count_total_directories = fields.Integer();
    count_total_files = fields.Integer();
    count_elements = fields.Integer();
    permission_read = fields.Boolean();
    permission_create = fields.Boolean();
    permission_write = fields.Boolean();
    permission_unlink = fields.Boolean();
    _records = [
        {
            id: 1,
            name: "Partner documents",
            storage_id: 1,
            res_model: "res.partner",
            res_id: 1001,
            count_directories: 0,
            count_files: 0,
            count_total_directories: 0,
            count_total_files: 0,
            count_elements: 0,
            permission_read: true,
            permission_create: true,
            permission_write: true,
            permission_unlink: true,
        },
    ];
}

const basePartnerRecords = mailModels.ResPartner._records;
class ResPartner extends mailModels.ResPartner {
    name = fields.Char();
    dms_directory_ids = fields.One2many({
        relation: "dms.directory",
        relation_field: "res_id",
    });
    _records = [
        ...basePartnerRecords,
        {id: 1001, name: "Azure Interior", dms_directory_ids: [1]},
    ];
}

mailModels.ResPartner = ResPartner;
defineMailModels();
defineModels([DmsStorage, DmsFieldTemplate, DmsDirectory]);

afterEach(() => {
    delete window.jQuery;
    delete window.$;
});

onRpc("dms.directory", "search_read_parents", ({kwargs}) => {
    // dms.directory.search_read_parents returns search_read records.
    return MockServer.env["dms.directory"].search_read(
        kwargs.domain,
        kwargs.fields,
    );
});

onRpc("dms.storage", "search_read", ({args, kwargs}) => {
    return MockServer.env["dms.storage"].search_read(kwargs.domain, args[1]);
});
test("DMS list renders its tree and directory preview", async () => {
    patchWithCleanup(serverState.view_info, {
        dms_list: {multi_record: true, display_name: "DMS List", icon: "folder"},
    });
    const loadedLibs = new Map();
    for (const url of [
        "/dms_field/static/lib/jquery/jquery.js",
        "/dms_field/static/lib/jsTree/jstree.js",
    ]) {
        const source = await globals.fetch(url).then((response) => response.text());
        new Function(source)();
        loadedLibs.set(url, Promise.resolve());
    }
    expect(window.jQuery).toBeInstanceOf(Function);
    expect(window.jQuery.fn.jstree).toBeInstanceOf(Function);
    patchWithCleanup(assets, {
        documentCaches: new WeakMap(),
        loadJS(url) {
            return loadedLibs.get(url);
        },
        loadCSS() {
            return Promise.resolve();
        },
    });
    patchWithCleanup(DmsListRenderer.prototype, {
        buildTreeConfig() {
            const config = super.buildTreeConfig(...arguments);
            config.core.worker = false; // Hoot replaces browser workers with a limited mock.
            return config;
        },
    });

    mockService("fileViewer", () => () => ({open() {}, close() {}}));
    await mountView({
        resModel: "res.partner",
        type: "form",
        resId: 1001,
        arch: `
            <form>
                <field name="name"/>
                <field name="dms_directory_ids" mode="dms_list">
                    <dms_list/>
                </field>
            </form>
        `,
    });
    expect(".o_field_x2many_dms_list .dms_treeview").toHaveCount(1);
    await waitFor("#directory_1.jstree-node > a:contains('Partner documents')");
    expect(".jstree-anchor:contains('Partner documents')").toHaveCount(1);
    await contains(".jstree-anchor:contains('Partner documents')").click();
    expect(".o_preview_directory h3").toHaveText("Partner documents");
});
