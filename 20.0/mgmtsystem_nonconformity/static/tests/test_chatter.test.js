import {
    STORE_FETCH_ROUTES,
    click,
    contains,
    listenStoreFetch,
    mailModels,
    onRpcBefore,
    openFormView,
    start,
    startServer,
    waitStoreFetch,
} from "@mail/../tests/mail_test_helpers";

import {defineModels, mockService} from "@web/../tests/web_test_helpers";
import {describe, expect, test} from "@odoo/hoot";

describe.current.tags("desktop", "mgmtsystem_nonconformity");

class MailThreadNonConformity extends mailModels.MailThread {
    _store_thread_fields(res, {request_list = []} = {}) {
        super._store_thread_fields(...arguments);
        if (request_list) {
            res.attr("non_conformity_count", 0);
        }
    }
}

defineModels({...mailModels, MailThread: MailThreadNonConformity});

test("simple chatter on a record", async () => {
    const pyEnv = await startServer();
    onRpcBefore((route, args) => {
        if (
            (route.startsWith("/mail") || route.startsWith("/discuss")) &&
            !STORE_FETCH_ROUTES.includes(route)
        ) {
            expect.step(`${route} - ${JSON.stringify(args)}`);
        }
    });
    listenStoreFetch(undefined, {logParams: ["mail.thread", "/mail/thread/messages"]});
    await start();
    await waitStoreFetch([
        "init_messaging",
        "failures",
        "systray_get_activities",
        "/mail/messaging_menu/initialize_counters",
    ]);
    const partnerId = pyEnv["res.partner"].create({name: "John Doe"});
    await openFormView("res.partner", partnerId);
    await contains(".o-mail-Chatter-topbar");
    await contains(".o-mail-Thread");
    await waitStoreFetch([
        [
            "/mail/thread/messages",
            {
                thread_id: partnerId,
                thread_model: "res.partner",
                fetch_params: {limit: 30},
            },
        ],
        [
            "mail.thread",
            {
                access_params: {},
                request_list: [
                    "activities",
                    "attachments",
                    "contact_fields",
                    "defaultSubject",
                    "followers",
                    "has_pinned_messages",
                    "scheduledMessages",
                    "showSubjectInSmallComposer",
                    "suggestedRecipients",
                    "suggestedSubject",
                ],
                thread_id: partnerId,
                thread_model: "res.partner",
            },
        ],
    ]);
    await contains(".o_ChatterTopbar_buttonNonConformities");
});

test("non conformities button opens the thread list of the record", async () => {
    const pyEnv = await startServer();
    const partnerId = pyEnv["res.partner"].create({name: "John Doe"});
    mockService("action", {
        doAction(action, options) {
            if (action === "mgmtsystem_nonconformity.open_mgmtsystem_nonconformity_thread_list") {
                expect.step(`doAction ${action}`);
                expect(options).toEqual({
                    additionalContext: {
                        id: partnerId,
                        mgmtsystem_nonconformity: "res.partner",
                    },
                });
                return;
            }
            return super.doAction(...arguments);
        },
    });
    await start();
    await openFormView("res.partner", partnerId);
    await contains(".o_ChatterTopbar_buttonNonConformities");
    await click(".o_ChatterTopbar_buttonNonConformities");
    await expect.waitForSteps([
        "doAction mgmtsystem_nonconformity.open_mgmtsystem_nonconformity_thread_list",
    ]);
});
