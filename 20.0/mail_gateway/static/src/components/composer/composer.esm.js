import { Composer } from "@mail/core/common/composer";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { prettifyMessageContent } from "@mail/utils/common/format";

patch(Composer.prototype, {
    get SEND_TEXT() {
        if (this.props.type === "gateway" && !this.props.composer.message) {
            return _t("Send gateway");
        }
        return super.SEND_TEXT;
    },
    get placeholder() {
        if (
            this.thread?.model !== "discuss.channel" &&
            !this.props.placeholder &&
            this.props.type === "gateway"
        ) {
            return _t("Send a message to a gateway...");
        }
        return super.placeholder;
    },
    get isSendButtonDisabled() {
        const isSendButtonDisabled = super.isSendButtonDisabled;
        if (this.props.type !== "gateway") {
            return isSendButtonDisabled;
        }
        return isSendButtonDisabled || !this.thread?.gateway_notifications?.length;
    },
    onFocusin() {
        super.onFocusin(...arguments);
        if (this.props.type !== "gateway" && this.thread) {
            this.thread.gateway_notifications = [];
        }
    },
    async onClickFullComposerGetAction() {
        if (this.props.type !== "gateway") {
            return super.onClickFullComposerGetAction(...arguments);
        }
        const attachmentIds = this.props.composer.attachments.map(
            (attachment) => attachment.id
        );
        const body = this.props.composer.composerText;
        const validMentions = this.store.getMentionsFromText(body, {
            mentionedPartners: this.props.composer.mentionedPartners,
            thread: this.thread,
        });
        const gatewayPartnerIds = this.thread.gateway_followers.map((follower) => follower.id);
        const gatewayChannelIds = this.thread.gateway_followers.flatMap((follower) =>
            follower.gateway_channels.map((channel) => channel?.id)
        );
        const context = {
            default_attachment_ids: attachmentIds,
            default_body: await prettifyMessageContent(body, validMentions),
            default_model: this.thread.model,
            default_partner_ids: this.thread.suggestedRecipients
                .filter((recipient) => recipient.partner_id)
                .map((recipient) => recipient.partner_id.id),
            default_res_ids: [this.thread.id],
            default_subtype_xmlid: "mail.mt_comment",
            default_wizard_partner_ids: [...new Set(gatewayPartnerIds)],
            default_wizard_channel_ids: [...new Set(gatewayChannelIds)],
            is_full_composer: true,
        };
        const action = {
            name: _t("Gateway message"),
            type: "ir.actions.act_window",
            res_model: "mail.compose.gateway.message",
            view_mode: "form",
            views: [[false, "form"]],
            target: "new",
            context,
        };
        const options = {
            onClose: (args) => {
                const isDiscard = args?.dismiss || args?.special;
                if (!isDiscard && this.thread.type === "mailbox") {
                    this.store.notifySendFromMailbox(this.thread.displayName);
                }
                if (!isDiscard) {
                    this.clear();
                }
                this.props.composer.replyToMessage = undefined;
                this.onCloseFullComposerCallback(isDiscard);
            },
        };
        return { action, options };
    },
});
