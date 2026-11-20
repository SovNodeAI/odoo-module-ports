/* Copyright 2026 Tecnativa
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html). */
import {patch} from "@web/core/utils/patch";
import {Many2OneField} from "@web/views/fields/many2one/many2one_field";

patch(Many2OneField.prototype, {
    // Odoo 20: the template of the field is only <Many2One/>, and the list of
    // props of Many2One is closed (subclasses in other modules declare their
    // own). So the condition the 19.0 template carried lives here, on the field,
    // and Many2One itself is left as it is.
    get isWeighingQuantField() {
        return (
            this.props.record.resModel === "weighing.wizard" &&
            this.props.name === "quant_id"
        );
    },
    get showClearQuantButton() {
        return (
            !this.props.readonly &&
            this.isWeighingQuantField &&
            this.props.record.data.quant_id
        );
    },
    get weighingQuantM2oProps() {
        // The field shares its row with the button: let it take the width.
        const props = this.m2oProps;
        return {...props, cssClass: `${props.cssClass || ""} flex-grow-1`.trim()};
    },
    async onClickClearQuant(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        const changes = {
            [this.props.name]: false,
            lot_id: false,
        };
        if (this.props.update) {
            await this.props.update(changes);
        } else {
            await this.props.record.update(changes);
        }
    },
});
