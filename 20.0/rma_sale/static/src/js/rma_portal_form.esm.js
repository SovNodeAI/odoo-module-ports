/* Copyright 2021 Tecnativa - David Vidal
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

export class PortalRmaSale extends Interaction {
    static selector = "#form-request-rma";

    dynamicContent = {
        ".rma-operation": { "t-on-change": this.onChangeOperationId },
        "#delivery-rma-qty input": { "t-on-change": this.onChangeQty },
        ".o_rma_portal_shipping_card": { "t-on-click": this.onChangeShippingAddress },
    };

    setup() {
        this.submitEl = this.el.querySelector("button[type='submit']");
        this.rowsIds = [...this.el.querySelectorAll("[name*='-operation_id']")].map(
            (el) => el.name.replace("-operation_id", "")
        );
        // We'll build an object that will ease the form check. It could be further
        // extended with additional checks.
        this.rows = {};
        for (const id of this.rowsIds) {
            this.rows[id] = {
                commentEl: this.el.querySelector(`#comment-${id}`),
                commentInputEl: this.el.querySelector(`[name='${id}-description']`),
                operationEl: this.el.querySelector(`[name='${id}-operation_id']`),
                qtyEl: this.el.querySelector(`[name='${id}-quantity']`),
            };
        }
    }

    start() {
        this.checkCanSubmit();
    }

    /**
     * @private
     * @param {Object} row: the form row structure
     */
    showComment(row) {
        if (row.commentEl) {
            row.commentEl.classList.add("show");
            if (row.commentInputEl) {
                row.commentInputEl.focus();
            }
        }
    }

    /**
     * @private
     * @param {Object} row: the form row structure
     */
    hideComment(row) {
        if (row.commentEl) {
            row.commentEl.classList.remove("show");
        }
    }

    /**
     * We should be able to submit only when an operation is selected and a
     * quantity entered in a row at least.
     * @private
     */
    canSubmit() {
        for (const id of this.rowsIds) {
            const row = this.rows[id];
            if (
                row &&
                // Qty greater than 0
                row.qtyEl &&
                row.qtyEl.value &&
                Number(row.qtyEl.value) &&
                // An operation is defined
                row.operationEl &&
                row.operationEl.value
            ) {
                return true;
            }
        }
        return false;
    }

    /**
     * Checked every time we change the quantity or the operation and at start
     *
     * @private
     */
    checkCanSubmit() {
        this.submitEl.disabled = !this.canSubmit();
    }

    /**
     * @private
     * @param {InputEvent} ev
     */
    onChangeOperationId(ev) {
        // Toggle comment on or off if an operation is requested
        const id = ev.currentTarget.name.replace("-operation_id", "");
        const row = this.rows[id];
        if (row && row.operationEl && row.operationEl.value) {
            this.showComment(row);
        } else if (row) {
            this.hideComment(row);
        }
        this.checkCanSubmit();
    }

    /**
     * @private
     */
    onChangeQty() {
        this.checkCanSubmit();
    }

    /**
     * @private
     * @param {MouseEvent} ev
     */
    onChangeShippingAddress(ev) {
        const cardEl = ev.currentTarget;
        const containerEl = cardEl.parentElement;
        for (const inputEl of containerEl.querySelectorAll("input")) {
            inputEl.checked = false;
        }
        for (const el of containerEl.querySelectorAll(".o_rma_portal_shipping_card")) {
            el.classList.remove("bg-primary", "text-primary");
        }
        const inputEl = cardEl.querySelector("input");
        if (inputEl) {
            inputEl.checked = true;
        }
        cardEl.classList.add("bg-primary", "text-primary");
    }
}

registry.category("public.interactions").add("rma_sale.portal_rma_sale", PortalRmaSale);
