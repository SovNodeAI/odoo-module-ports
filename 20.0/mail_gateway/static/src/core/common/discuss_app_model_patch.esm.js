import { MessagingMenu } from "@mail/core/public_web/messaging_menu/messaging_menu_model";
import { _t } from "@web/core/l10n/translation";
import { fields } from "@mail/model/export";
import { patch } from "@web/core/utils/patch";

patch(MessagingMenu.prototype, {
    setup() {
        super.setup(...arguments);
        this.gatewayTab = fields.One("MessagingMenuTab", {
            compute() {
                return {
                    id: "gateway",
                    recordType: "discuss.channel",
                    includesChannel: (channel) =>
                        channel.channel_type === "gateway" &&
                        Boolean(
                            channel.isLocallyPinned ||
                                channel.self_member_id?.is_pinned ||
                                channel.message_needaction_counter
                        ),
                    icon: "travel",
                    sequence: 35,
                    label: _t("Gateway"),
                    emptyState: { title: _t("No gateway conversations") },
                    actions: this.store.env.services.action
                        ? [
                              {
                                  id: "new_gateway_channel",
                                  text: _t("Gateway"),
                                  icon: "add",
                                  title: _t("Search Gateway Channel"),
                                  onClick: () =>
                                      this.store.env.services.action.doAction({
                                          type: "ir.actions.act_window",
                                          name: _t("Search Gateway Channel"),
                                          res_model: "discuss.channel",
                                          domain: [["channel_type", "=", "gateway"]],
                                          context: {
                                              default_channel_type: "gateway",
                                              default_gateway_id:
                                                  this.store.Gateway.records.values().next()
                                                      .value?.id,
                                          },
                                          views: [[false, "list"], [false, "form"]],
                                          view_mode: "list,form",
                                      }),
                              },
                          ]
                        : [],
                };
            },
            eager: true,
        });
    },
});
