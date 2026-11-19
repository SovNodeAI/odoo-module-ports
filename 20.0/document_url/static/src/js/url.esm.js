/** @odoo-module **/

import {AttachmentList} from "@mail/core/common/attachment_list";
import {Chatter} from "@mail/chatter/web_portal_project/chatter";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";

patch(Chatter.prototype, {
    setup() {
        super.setup(...arguments);
        this.action = useService("action");
    },
    _onAddUrl(event) {
        event.preventDefault();
        event.stopPropagation();
        const thread = this.thread();
        this.action.doAction("document_url.action_ir_attachment_add_url", {
            additionalContext: {
                active_id: thread.id,
                active_ids: [thread.id],
                active_model: thread.model,
            },
            onClose: async () => {
                await this.load(thread, ["attachments"]);
            },
        });
    },
});

patch(AttachmentList.prototype, {
    /**
     * A URL attachment has no file to download: it is opened through its link.
     *
     * @param {Object} attachment
     * @returns {Boolean}
     */
    canDownload(attachment) {
        return (
            super.canDownload(attachment) && attachment.mimetype !== "application/link"
        );
    },
});
