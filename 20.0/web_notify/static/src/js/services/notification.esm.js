import {NotificationPlugin} from "@web/core/notifications/notification_plugin";
import {patch} from "@web/core/utils/patch";

// Types accepted by the core notification schema.
const CORE_NOTIFICATION_TYPES = ["warning", "danger", "success", "info"];

patch(NotificationPlugin.prototype, {
    add(message, options = {}) {
        if (options.type && !CORE_NOTIFICATION_TYPES.includes(options.type)) {
            // The core notification schema only knows the types above. The
            // "default" type (and any other custom type) has no core
            // equivalent, so render it with a neutral style rather than with
            // the core fallback type.
            options = {
                ...options,
                type: "warning",
                className: `${options.className || ""} o_web_notify_default`.trim(),
            };
        }
        return super.add(message, options);
    },
});
