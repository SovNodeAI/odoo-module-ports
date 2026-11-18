import { Notification } from "@mail/core/common/notification_model";
import { MessageNotificationPopover } from "@mail/core/common/message_notification_popover";
import { patch } from "@web/core/utils/patch";

patch(MessageNotificationPopover.prototype, {
    get recipientsData() {
        return super.recipientsData.map((recipient) => {
            if (recipient.notification?.notification_type !== "gateway") {
                return recipient;
            }
            return {
                ...recipient,
                name: recipient.notification.channel_name,
                email: false,
            };
        });
    },
});

patch(Notification.prototype, {
    get icon() {
        if (this.gateway_type) {
            return `fa fa-${this.gateway_type}`;
        }
        return super.icon;
    },
    get statusIcon() {
        if (!this.gateway_type) {
            return super.statusIcon;
        }
        // It can be overriden on the gateway implementation
        switch (this.notification_status) {
            case "process":
                return "hourglass_bottom";
            case "pending":
                return "send";
            case "sent":
                return "check";
            case "bounce":
                return "priority_high";
            case "exception":
                return "cancel";
            case "ready":
                return "send";
            case "canceled":
                return "delete";
        }
        return "";
    },
    get statusClass() {
        if (!this.gateway_type) {
            return super.statusClass;
        }
        switch (this.notification_status) {
            case "sent":
                return "text-success";
            case "bounce":
            case "exception":
                return "text-danger oi-filled";
        }
        return "";
    },
});
