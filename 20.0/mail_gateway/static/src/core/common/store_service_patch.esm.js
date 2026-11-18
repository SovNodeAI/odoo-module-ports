import { Store } from "@mail/core/common/store_service";
import { patch } from "@web/core/utils/patch";

patch(Store.prototype, {
    async getMessagePostParams(params) {
        const postParams = await super.getMessagePostParams(...arguments);
        if (params.thread.gateway_notifications) {
            postParams.post_data.gateway_notifications = params.thread.gateway_notifications;
        }
        return postParams;
    },
});
