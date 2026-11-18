import { DiscussChannel } from "@mail/discuss/core/common/discuss_channel_model";
import { Thread } from "@mail/core/common/thread_model";
import { fields } from "@mail/model/export";
import { patch } from "@web/core/utils/patch";
import { imageUrl } from "@web/core/utils/urls";

patch(Thread.prototype, {
    setup() {
        super.setup(...arguments);
        this.gateway_notifications = [];
        this.gateway_followers = fields.Many("res.partner");
    },
    /** @param {Object} data */
    update(data) {
        super.update(...arguments);
        if ("gateway_id" in data && this.channel_type === "gateway") {
            this.gateway = data.gateway_id;
        }
    },
});

patch(DiscussChannel.prototype, {
    setup() {
        super.setup(...arguments);
        this.gateway = fields.One("Gateway");
        this.operator = fields.One("res.partner");
    },
    get allowedToLeaveChannelTypes() {
        // Allow leaving the thread if it is a gateway channel.
        return [...super.allowedToLeaveChannelTypes, "gateway"];
    },
    get chatChannelTypes() {
        return [...super.chatChannelTypes, "gateway"];
    },
    get hasMemberList() {
        return this.channel_type === "gateway" || super.hasMemberList;
    },
    get avatarUrl() {
        if (this.channel_type !== "gateway") {
            return super.avatarUrl;
        }
        return imageUrl("discuss.channel", this.id, "avatar_128", {
            unique: this.avatar_cache_key,
        });
    },
});
