import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { sprintf } from "@web/core/utils/strings";
import { humanSize } from "@web/core/utils/binary";
import { useService } from "@web/core/utils/hooks";

export class NewTicket extends Interaction {
    static selector = "form[action='/submitted/ticket']";

    setup() {
        this.notification = useService("notification");
    }

    start() {
        const attachmentInput = this.el.querySelector("#attachment");
        if (attachmentInput) {
            this.addListener(attachmentInput, "change", this._onChangeAttachment);
        }
    }

    _onChangeAttachment(ev) {
        ev.preventDefault();
        const attachmentInput = this.el.querySelector("#attachment");
        const maxUploadSize = attachmentInput.getAttribute("max_upload_size");
        const dt = new DataTransfer();
        for (const file of attachmentInput.files) {
            if (file.size > maxUploadSize) {
                this.notification.add(
                    sprintf(
                        _t("%s file exceed the maximum file size of %s."),
                        file.name,
                        humanSize(maxUploadSize)
                    ),
                    { title: _t("File upload"), type: "danger" }
                );
            } else {
                dt.items.add(file);
            }
        }
        attachmentInput.files = dt.files;
    }
}

registry.category("public.interactions").add("helpdesk_mgmt.new_ticket", NewTicket);
