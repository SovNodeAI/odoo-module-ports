import {Component, onWillStart, proxy, useProps} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class SendcloudOnboarding extends Component {
    static template = "sendcloud.Onboarding";
    props = useProps({});

    setup() {
        this.action = useService("action");
        this.orm = useService("orm");
        this.state = proxy({
            steps: null,
            onboardingState: null,
        });
        onWillStart(this.onWillStart);
    }

    async onWillStart() {
        const onboarding_data = await this.orm.call(
            "onboarding.onboarding",
            "get_sendcloud_onboarding_data",
            [],
            {}
        );
        this.state.steps = onboarding_data.steps;
        this.state.onboardingState = onboarding_data.onboarding_state;
    }

    async onboardingLinkClicked(step) {
        const action = await this.orm.call(
            "onboarding.onboarding.step",
            step.action,
            [],
            {}
        );
        this.action.doAction(action, {
            onClose: async () => {
                await this.onWillStart();
            },
        });
    }
}
