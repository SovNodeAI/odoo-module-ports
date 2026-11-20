import {BooleanField, booleanField} from "@web/views/fields/boolean/boolean_field";
import {CheckBox} from "@web/core/checkbox/checkbox";
import {onMounted, onPatched, signal, t, useProps} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
const {document} = globalThis;

export class BooleanButton extends BooleanField {
    static template = "product_configurator.BooleanButtonField";
    static components = {CheckBox};

    props = useProps({
        ...standardFieldProps,
        activeString: t.string(),
        inactiveString: t.string().optional(),
    });

    root = signal.ref();

    setup() {
        super.setup();

        onMounted(() => {
            this.updateConfigurableButton();
        });

        onPatched(() => {
            this.updateConfigurableButton();
        });
    }

    updateConfigurableButton() {
        const rootEl = this.root();
        if (!rootEl) {
            return;
        }
        this.text = this.state.value
            ? this.props.activeString
            : this.props.inactiveString;
        this.hover = this.state.value
            ? this.props.inactiveString
            : this.props.activeString;
        var val_color = this.state.value ? "text-success" : "text-danger";
        var hover_color = this.state.value ? "text-danger" : "text-success";

        const valSpan = document.createElement("span");
        valSpan.className = `o_stat_text o_boolean_button o_not_hover ${val_color}`;
        valSpan.textContent = this.text;

        const hoverSpan = document.createElement("span");
        hoverSpan.className = `o_stat_text o_boolean_button o_hover d-none ${hover_color}`;
        hoverSpan.textContent = this.hover;

        rootEl.innerHTML = "";
        rootEl.appendChild(valSpan);
        rootEl.appendChild(hoverSpan);
    }
}

export const BooleanButtonField = {
    ...booleanField,
    component: BooleanButton,
    extractProps: ({options}) => {
        return {
            activeString: options.active,
            inactiveString: options.inactive,
        };
    },
};

// Register the field component
registry.category("fields").add("boolean_button", BooleanButtonField);
