import {CardCompiler} from "@web/views/card/card_compiler";

export class AutomationKanbanCompiler extends CardCompiler {
    setup() {
        super.setup();
        this.compilers.push({
            selector: ".o_automation_kanban_child_add_button[t-att-trigger-type]",
            fn: this.compileHierarchyAddButton,
        });
    }
    compileHierarchyAddButton(el) {
        el.classList.add(this.constructor.ACTION_CLASS);
        el.setAttribute(
            "t-on-click",
            "() => __comp__.addNewChild({trigger_type: " +
                el.getAttribute("t-att-trigger-type") +
                "})"
        );
        return el;
    }
}
