import {Component, t, useProps} from "@odoo/owl";
import {PickingDoneCard} from "./picking_done_card.esm";

export class PickingDoneList extends Component {
    props = useProps({
        lines: t.array(),
        highlightedMoveId: t.or([t.number(), t.literal(null)]).optional(),
        onDeleteLine: t.function(),
    });

    get doneLines() {
        return this.props.lines.filter((line) => line.qty_picked > 0);
    }
}

PickingDoneList.template = "barcode_scanner.PickingDoneList";
PickingDoneList.components = {PickingDoneCard};
