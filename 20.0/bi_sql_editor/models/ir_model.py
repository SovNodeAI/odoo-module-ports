from odoo import models
from odoo.tools import sql


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    def _instanciate_attrs(self, field_data):
        attrs = super()._instanciate_attrs(field_data)
        if (
            attrs
            and field_data["model"].startswith("x_bi_sql_view.")
            and field_data["ttype"] in ("integer", "float")
        ):
            aggregator = self._get_bi_sql_view_aggregator(
                field_data["model"], field_data["name"]
            )
            if aggregator:
                attrs["aggregator"] = aggregator
        return attrs

    def _get_bi_sql_view_aggregator(self, model_name, field_name):
        # check the fields we need are defined on self, to stop it going
        # early on install / startup - particularly problematic during upgrade
        if "group_operator" not in sql.table_columns(self.env.cr, "bi_sql_view_field"):
            return False
        # Use SQL instead of ORM, as ORM might not be fully initialised -
        # we have no control over the order that fields are defined!
        # We are not concerned about user security rules.
        self.env.cr.execute(
            """
SELECT
    f.group_operator
FROM
    bi_sql_view v
    LEFT JOIN bi_sql_view_field f ON f.bi_sql_view_id = v.id
WHERE
    v.model_name = %s
    AND f.name = %s
;
            """,
            (model_name, field_name),
        )
        row = self.env.cr.fetchone()
        return row and row[0] or False
