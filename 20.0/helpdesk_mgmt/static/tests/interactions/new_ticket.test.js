/* Copyright 2026 SovNode AI
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import {expect, test} from "@odoo/hoot";
import {queryOne} from "@odoo/hoot-dom";
import {animationFrame} from "@odoo/hoot-mock";
import {setupInteractionWhiteList, startInteractions} from "@web/../tests/public/helpers";

setupInteractionWhiteList("helpdesk_mgmt.new_ticket");

test("Rejects attachments larger than the maximum upload size", async () => {
    await startInteractions(`
        <form action="/submitted/ticket">
            <input id="attachment" name="attachment" type="file" multiple="multiple" max_upload_size="5"/>
            <div id="attachment_information" style="display: none;"></div>
        </form>
    `);

    const attachmentInput = queryOne("#attachment");
    const selectedFiles = new DataTransfer();
    selectedFiles.items.add(new File(["small"], "small.txt", {type: "text/plain"}));
    selectedFiles.items.add(new File(["too large"], "large.txt", {type: "text/plain"}));
    attachmentInput.files = selectedFiles.files;
    attachmentInput.dispatchEvent(new Event("change", {bubbles: true}));
    await animationFrame();

    expect(attachmentInput.files).toHaveLength(1);
    expect(attachmentInput.files[0].name).toBe("small.txt");
    expect("#attachment_information").toBeVisible();
    expect("#attachment_information").toHaveText(
        "The selected file (9B) is over the maximum allowed file size (5B)."
    );

    const validFiles = new DataTransfer();
    validFiles.items.add(new File(["small"], "small.txt", {type: "text/plain"}));
    attachmentInput.files = validFiles.files;
    attachmentInput.dispatchEvent(new Event("change", {bubbles: true}));
    await animationFrame();

    expect(attachmentInput.files).toHaveLength(1);
    expect("#attachment_information").not.toBeVisible();
});
