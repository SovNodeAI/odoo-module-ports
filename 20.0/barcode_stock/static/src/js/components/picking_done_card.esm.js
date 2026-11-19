import {Component, t, useProps} from "@odoo/owl";

export class PickingDoneCard extends Component {
    props = useProps({
        line: t.object(),
        highlighted: t.boolean().optional(),
        onDelete: t.function(),
    });
}

PickingDoneCard.template = "barcode_scanner.PickingDoneCard";
