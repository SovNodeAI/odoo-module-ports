/** @odoo-module **/

import {Component, onWillStart, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {standardFieldProps} from "@web/views/fields/standard_field_props";

export class ReviewField extends Component {
    static template = "base_tier_validation.Collapse";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            collapse: false,
            reviews: [],
        });
        onWillStart(() => this._renderDropdown());
    }

    get resIds() {
        const value = this.props.record.data[this.props.name];
        return value ? value.currentIds : [];
    }

    /**
     * Make RPC and get current user's activity details
     * @private
     * @returns {Promise}
     */
    _getReviewData() {
        return this.orm
            .call("res.users", "get_reviews", [{res_ids: this.resIds}])
            .then((data) => {
                this.state.reviews = data;
            });
    }

    _renderDropdown() {
        return this._getReviewData();
    }

    onToggleCollapse(ev) {
        ev.preventDefault();
        this.state.collapse = !this.state.collapse;
    }
}

export const reviewField = {
    component: ReviewField,
    supportedTypes: ["one2many"],
};

registry.category("fields").add("tier_validation", reviewField);
