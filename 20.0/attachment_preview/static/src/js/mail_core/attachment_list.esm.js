import {canPreview, showPreview} from "../utils.esm";
import {AttachmentList} from "@mail/core/common/attachment_list";
import {patch} from "@web/core/utils/patch";

patch(AttachmentList.prototype, {
    _onPreviewAttachment(attachment, ev) {
        var target = ev?.currentTarget;
        var split_screen = target?.getAttribute("data-target") !== "new";
        showPreview(
            attachment.id,
            attachment.defaultSource,
            attachment.extension,
            attachment.name,
            split_screen,
            this.props.attachmentGroups.map((group) => group.attachment)
        );
    },

    _canPreviewAttachment(attachment) {
        return canPreview(attachment.extension);
    },
});
