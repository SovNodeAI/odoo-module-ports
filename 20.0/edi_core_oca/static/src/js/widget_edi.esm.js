import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {useService} from "@web/core/utils/hooks";

import {Component, t, useProps} from "@odoo/owl";

export class EdiConfigurationWidget extends Component {
    static template = "edi_core_oca.EdiConfigurationWidget";
    props = useProps({...standardFieldProps});

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
    }
    async onClick(ev, rule) {
        ev.preventDefault();
        ev.stopPropagation();
        var typeId = rule.type.id;
        const action = await this.orm.call(
            this.props.record.resModel,
            "edi_create_exchange_record",
            [[this.props.record.resId], typeId],
            {context: this.props.record.context}
        );
        this.action.doAction(action);
    }
    get info() {
        return this.props.record.data[this.props.name];
    }
}

registry.category("fields").add("edi_configuration", {
    component: EdiConfigurationWidget,
});
