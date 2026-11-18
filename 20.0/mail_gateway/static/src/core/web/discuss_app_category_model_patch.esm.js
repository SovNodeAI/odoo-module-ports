import { compareDatetime } from "@mail/utils/common/misc";
import { threadCompareRegistry } from "@mail/core/common/thread_compare";

threadCompareRegistry.add(
    "mail_gateway.gateway-last-interest",
    (thread1, thread2) => {
        if (thread1.channel_type !== "gateway" && thread2.channel_type !== "gateway") {
            return;
        }
        return (
            compareDatetime(thread2.channel?.lastInterestDt, thread1.channel?.lastInterestDt) ||
            thread2.id - thread1.id
        );
    },
    { sequence: 35 }
);
