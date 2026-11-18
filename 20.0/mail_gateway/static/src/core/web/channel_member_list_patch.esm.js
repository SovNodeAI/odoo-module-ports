import {ChannelMember} from "@mail/discuss/core/common/channel_member";
import {patch} from "@web/core/utils/patch";

// As in 19.0: a member who is not a user (a contact reached through a gateway)
// has no card to open. For every other member Odoo's own handler runs.
patch(ChannelMember.prototype, {
    onClickAvatar(ev, {memberAtRender}) {
        if (!memberAtRender.partner_id?.main_user_id?.id) {
            return;
        }
        return super.onClickAvatar(...arguments);
    },
});
