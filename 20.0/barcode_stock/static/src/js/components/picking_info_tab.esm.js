import {Component, t, useProps} from "@odoo/owl";

/**
 * Wrap a typed note as a paragraph, escaping it first: an operator may well
 * write "5 < 10", and the note is stored in an HTML field.
 */
function noteToHtml(text) {
    const escaped = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    return `<p>${escaped}</p>`;
}

export class PickingInfoTab extends Component {
    props = useProps({
        picking: t.object(),
        pickingTypeCode: t.string().optional(),
        progressLabel: t.string().optional(),
        onSelectResponsible: t.function().optional(),
    });

    get notePlainText() {
        const note = this.props.picking?.note;
        if (!note) return "";
        const tmp = document.createElement("div");
        tmp.innerHTML = note;
        return tmp.textContent || tmp.innerText || "";
    }

    onNoteInput(ev) {
        const text = ev.target.value.trim();
        this.props.picking.note = text ? noteToHtml(text) : "";
    }

    onSelectResponsible() {
        this.props.onSelectResponsible?.();
    }
}

PickingInfoTab.template = "barcode_scanner.PickingInfoTab";
