import {Component, onWillUnmount, signal, useProps} from "@odoo/owl";
import {sprintf} from "@web/core/utils/strings";

export class AttachmentPreviewWidget extends Component {
    static template = "attachment_preview.AttachmentPreviewWidget";
    props = useProps({});

    currentRef = signal.ref();
    iframeRef = signal.ref();
    rootRef = signal.ref();

    setup() {
        super.setup();
        this.state = signal.Object({activeIndex: 0});
        this.attachments = [];
        this._onOpenPreview = ({detail: {attachment_id, attachment_info_list}}) =>
            this._onAttachmentPreview(attachment_id, attachment_info_list);
        this._onHidePreview = () => this.hide();
        this.env.bus.addEventListener("open_attachment_preview", this._onOpenPreview);
        this.env.bus.addEventListener("hide_attachment_preview", this._onHidePreview);
        onWillUnmount(() => {
            this.env.bus.removeEventListener("open_attachment_preview", this._onOpenPreview);
            this.env.bus.removeEventListener("hide_attachment_preview", this._onHidePreview);
        });
    }

    _onCloseClick() {
        this.hide();
    }

    _onPreviousClick() {
        this.previous();
    }

    _onNextClick() {
        this.next();
    }

    _onPopoutClick() {
        if (!this.attachments[this.state().activeIndex]) return;

        window.open(this.attachments[this.state().activeIndex].previewUrl);
    }

    next() {
        var index = this.state().activeIndex + 1;
        if (index >= this.attachments.length) {
            index = 0;
        }
        this.state().activeIndex = index;
        this.updatePaginator();
        this.loadPreview();
    }

    previous() {
        var index = this.state().activeIndex - 1;
        if (index < 0) {
            index = this.attachments.length - 1;
        }
        this.state().activeIndex = index;
        this.updatePaginator();
        this.loadPreview();
    }

    show() {
        this.rootRef()?.classList.remove("d-none");
    }

    hide() {
        this.rootRef()?.classList.add("d-none");
    }

    updatePaginator() {
        var value = sprintf(
            "%s / %s",
            this.state().activeIndex + 1,
            this.attachments.length
        );
        if (this.currentRef()) {
            this.currentRef().textContent = value;
        }
    }

    loadPreview() {
        if (this.attachments.length === 0) {
            this.iframeRef()?.setAttribute("src", "about:blank");
            return;
        }
        var att = this.attachments[this.state().activeIndex];
        this.iframeRef()?.setAttribute("src", att.previewUrl);
    }

    setAttachments(attachments, active_attachment_id) {
        this.attachments = attachments;
        if (!attachments) return;
        for (let i = 0; i < attachments.length; ++i) {
            if (parseInt(attachments[i].id, 10) === active_attachment_id) {
                this.state().activeIndex = i;
            }
        }
        this.updatePaginator();
        this.loadPreview();
    }

    _onAttachmentPreview(attachment_id, attachment_info_list) {
        this.setAttachments(attachment_info_list, attachment_id);
        this.show();
    }
}
