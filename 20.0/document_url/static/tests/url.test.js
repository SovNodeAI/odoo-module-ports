/* Copyright 2026 SovNode AI
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import {
    contains,
    defineMailModels,
    openFormView,
    start,
    startServer,
} from "@mail/../tests/mail_test_helpers";
import { describe, expect, test } from "@odoo/hoot";

describe.current.tags("desktop");
defineMailModels();

async function openChatterWithUrlAttachment() {
    const pyEnv = await startServer();
    const partnerId = pyEnv["res.partner"].create({ name: "Partner" });
    pyEnv["ir.attachment"].create({
        mimetype: "application/link",
        name: "Odoo",
        type: "url",
        url: "https://www.odoo.com",
        res_id: partnerId,
        res_model: "res.partner",
    });
    await start();
    await openFormView("res.partner", partnerId, {
        arch: `
            <form>
                <sheet></sheet>
                <chatter open_attachments="True"/>
            </form>`,
    });
    await contains(".o-mail-AttachmentBox");
    return { partnerId, pyEnv };
}

test("url attachment is rendered as a link chip in the chatter", async () => {
    await openChatterWithUrlAttachment();
    await contains(".o_attachment_url_chip");
    await contains(".o_attachment_url_chip a[href='https://www.odoo.com']");
    await contains(".o_attachment_url_chip:has(:text('Odoo'))");
    await contains("button:text('Add URL')");
});

test("url attachment is not offered for download", async () => {
    await openChatterWithUrlAttachment();
    await contains(".o_attachment_url_chip");
    // The card of a regular attachment offers a download button; a URL
    // attachment must not, it is opened through its link instead.
    expect(document.querySelector(".o_attachment_url_chip [title='Download']")).toBe(null);
    expect(document.querySelector(".o_attachment_url_chip a[href='https://www.odoo.com']")).not.toBe(
        null
    );
});
