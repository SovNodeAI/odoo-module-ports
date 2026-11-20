/* global sendcloud */
import {Component, onWillStart, signal, useProps} from "@odoo/owl";
import {WarningDialog} from "@web/core/errors/error_dialogs";
import {_t} from "@web/core/l10n/translation";
import {loadJS} from "@web/core/assets";
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {useInputField} from "@web/views/fields/input_field_hook";
import {useService} from "@web/core/utils/hooks";

export class ServicePointSelectorField extends Component {
    static template = "delivery_sendcloud_oca.ServicePointField";
    props = useProps(standardFieldProps);
    inputRef = signal.ref();

    setup() {
        useInputField({
            ref: this.inputRef,
            getValue: () => this.props.record.data[this.props.name] || "",
        });
        this.dialog = useService("dialog");
        onWillStart(async () => {
            loadJS("/delivery_sendcloud_oca/static/src/lib/sendcloud/api.min.js");
        });
    }

    async onClearClick() {
        await this.props.record.update({[this.props.name]: ""});
    }

    async _onServicePointError(errors) {
        const irrelevantErrors = ["Closed"];
        const relevantErrors = errors.filter((error) => !irrelevantErrors.includes(error));

        if (relevantErrors.length) {
            this.dialog.add(WarningDialog, {
                title: _t("Failure in opening Service Point Selector"),
                message: relevantErrors.join("\n"),
            });
        }
    }

    async _onServicePointSelected(servicePoint) {
        await this.props.record.update({
            [this.props.name]: JSON.stringify(servicePoint),
        });
    }

    async onInputClick() {
        const value = this.props.record.data.sendcloud_sp_details;
        if (!value) {
            return "";
        }

        const parsedValue = JSON.parse(value);
        sendcloud.servicePoints.open(
            {
                apiKey: parsedValue.api_key,
                country: parsedValue.country,
                postalCode: parsedValue.postalcode,
                language: parsedValue.language,
                carriers: [parsedValue.carrier],
            },
            this._onServicePointSelected.bind(this),
            this._onServicePointError.bind(this)
        );
    }

    get sp_name() {
        try {
            return JSON.parse(this.props.record.data[this.props.name]).name;
        } catch {
            return "";
        }
    }

    get street() {
        try {
            return JSON.parse(this.props.record.data[this.props.name]).street;
        } catch {
            return "";
        }
    }

    get house_number() {
        try {
            return JSON.parse(this.props.record.data[this.props.name]).house_number;
        } catch {
            return "";
        }
    }

    get postal_code() {
        try {
            return JSON.parse(this.props.record.data[this.props.name]).postal_code;
        } catch {
            return "";
        }
    }

    get city() {
        try {
            return JSON.parse(this.props.record.data[this.props.name]).city;
        } catch {
            return "";
        }
    }
}

export const servicePointSelectorField = {
    component: ServicePointSelectorField,
    supportedTypes: ["text"],
    displayName: _t("Service Point Selector"),
};

registry
    .category("fields")
    .add("sendcloud_service_point_selector", servicePointSelectorField);
