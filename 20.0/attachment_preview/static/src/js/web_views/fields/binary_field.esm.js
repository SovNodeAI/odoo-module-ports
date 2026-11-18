import {canPreview, showPreview} from "../../utils.esm";
import {BinaryField} from "@web/views/fields/binary/binary_field";
import {_t} from "@web/core/l10n/translation";
import {onMounted} from "@odoo/owl";
import {patch} from "@web/core/utils/patch";
import {sprintf} from "@web/core/utils/strings";
import {useService} from "@web/core/utils/hooks";

patch(BinaryField.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        onMounted(this._preview_onMounted);
    },

    async _preview_onMounted() {
        if (this.props.record.resId) {
            var extension = await this.orm.call(
                "ir.attachment",
                "get_binary_extension",
                [
                    this.props.record.resModel,
                    this.props.record.resId,
                    this.props.name,
                    this.props.fileNameField,
                ]
            );
            if (canPreview(extension)) {
                this._renderPreviewButton(extension);
            }
        }
    },

    _renderPreviewButton(extension) {
        // Add a button same as standard download one.
        var rootEl = this.__owl__?.bdom?.el;
        if (!rootEl) return;
        var dl_button = rootEl.querySelector("button[data-icon='download']");
        if (!dl_button) return;
        var preview_button = document.createElement("button");
        preview_button.classList.add("btn", "btn-link", "oi", "o_preview_file_button");
        preview_button.setAttribute("data-icon", "open_in_new");
        preview_button.setAttribute("data-tooltip", "Preview");
        preview_button.setAttribute("aria-label", "Preview");
        preview_button.setAttribute("data-extension", extension);
        dl_button.after(preview_button);
        preview_button.addEventListener("click", this._onPreview.bind(this));
    },

    _onPreview(event) {
        showPreview(
            null,
            sprintf(
                "/web/content?model=%s&field=%s&id=%s",
                this.props.record.resModel,
                this.props.name,
                this.props.record.resId
            ),
            event.currentTarget.getAttribute("data-extension"),
            sprintf(_t("Preview %s"), this.fileName),
            false,
            null
        );
        event.stopPropagation();
    },
});
