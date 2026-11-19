import {Component, t, useProps} from "@odoo/owl";
import {PickingMoveCard} from "./picking_move_card.esm";
import {isMovePending} from "@barcode_stock/js/utils/move_progress.esm";
import {roundQty} from "@barcode_stock/js/utils/quantity.esm";

export class PickingMoveList extends Component {
    props = useProps({
        moves: t.array(),
        moveLines: t.array().optional(),
        moveStatsById: t.object().optional(),
        highlightedMoveId: t.or([t.number(), t.literal(null)]).optional(),
        onOpenWizard: t.function(),
    });

    showMove(move) {
        return isMovePending(move);
    }

    getMoveStats(move) {
        return (
            this.props.moveStatsById?.[move.id] || {
                demandQty: move.product_uom_qty || move.quantity || 0,
                doneQty: move.qty_done_total || 0,
                remainingQty: Math.max(
                    roundQty((move.quantity || 0) - (move.qty_done_total || 0)),
                    0
                ),
                completionLabel: "0%",
            }
        );
    }
}

PickingMoveList.template = "barcode_scanner.PickingMoveList";
PickingMoveList.components = {PickingMoveCard};
