/** @odoo-module **/

import {Component, onWillStart, useState} from "@odoo/owl";
import {Dropdown} from "@web/core/dropdown/dropdown";
import {registry} from "@web/core/registry";
import {useDropdownState} from "@web/core/dropdown/dropdown_hooks";
import {useService} from "@web/core/utils/hooks";

export class ReviewMenu extends Component {
    static components = {Dropdown};
    static props = [];
    static template = "base_tier_validation.ReviewMenu";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.busService = useService("bus_service");
        this.dropdown = useDropdownState();
        this.state = useState({
            reviews: [],
            reviewCounter: 0,
        });
        onWillStart(() => this._updateReviewPreview());
        this.busService.subscribe("base.tier.validation/updated", () =>
            this._updateReviewPreview()
        );
        this.busService.start();
    }

    /**
     * Make RPC and get current user's activity details
     * @private
     * @returns {Promise}
     */
    _getReviewData() {
        return this.orm.call("res.users", "review_user_count").then((data) => {
            this.state.reviews = data;
            this.state.reviewCounter = data.reduce(
                (total, review) => total + review.pending_count,
                0
            );
        });
    }

    /**
     * Update(render) activity system tray view on activity updation.
     * @private
     */
    _updateReviewPreview() {
        return this._getReviewData();
    }

    /**
     * Redirect to particular model view
     * @private
     * @param {Object} review
     */
    _onReviewFilterClick(review) {
        const domain = [["can_review", "=", true]];
        if (review.active_field) {
            domain.push(["active", "in", [true, false]]);
        }
        this.dropdown.close();
        this.action.doAction({
            type: "ir.actions.act_window",
            name: review.name,
            res_model: review.model,
            views: [
                [false, "list"],
                [false, "form"],
            ],
            search_view_id: [false],
            domain,
            context: {},
        });
    }
}

export const systrayItem = {
    Component: ReviewMenu,
};

registry
    .category("systray")
    .add("base_tier_validation.ReviewMenu", systrayItem, {sequence: 24});
