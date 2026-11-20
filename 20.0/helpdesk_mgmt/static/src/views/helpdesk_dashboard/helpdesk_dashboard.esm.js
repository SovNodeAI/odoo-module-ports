import {Component, onWillStart, proxy, useProps} from "@odoo/owl";
import {useBus, useService} from "@web/core/utils/hooks";
import {SIZES} from "@web/core/ui/ui_utils";
import {ViewButton} from "@web/views/view_button/view_button";

export class HelpdeskDashboard extends Component {
    static template = "helpdesk_mgmt.HelpdeskDashboard";
    props = useProps();
    static components = {ViewButton};
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.uiService = useService("ui");
        useBus(this.uiService.bus, "resize", this.updateGridTemplateColumns.bind(this));
        this.state = proxy({
            gridTemplateColumns: this._getGridTemplateColumns(),
        });
        onWillStart(async () => {
            this.helpdeskData = await this.orm.call(
                "helpdesk.ticket.team",
                "retrieve_dashboard"
            );
        });
    }
    clickParams(section) {
        if (section.action) {
            return {name: section.action, type: "action"};
        }
        return {};
    }

    _getGridTemplateColumns() {
        switch (this.uiService.size) {
            case SIZES.XS:
                return 2;
            // The 19.0 code had "case SIZES.VSM: return 3;" here. VSM stopped being
            // a size in Odoo 19, so on 19.0 that case never matched and every
            // size between XS and XXL showed four columns. Kept that way.
            case SIZES.XXL:
                return 6;
            default:
                return 4;
        }
    }

    updateGridTemplateColumns() {
        this.state.gridTemplateColumns = this._getGridTemplateColumns();
    }
}
