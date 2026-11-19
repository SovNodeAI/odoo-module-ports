import {
    BadgesMany2oneField,
    badgesMany2oneField,
} from "@web/views/fields/badges_many2one/badges_many2one_field";
import {registry} from "@web/core/registry";

registry.category("fields").add("selection_badge_uncheck", badgesMany2oneField);
