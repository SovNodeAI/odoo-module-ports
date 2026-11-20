# Copyright 2013 Nicolas Bessi (Camptocamp SA)
# Copyright 2014 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ResUser(models.Model):
    _inherit = "res.users"

    @api.model
    def default_get(self, fields_list):
        """Invert name when getting default values."""
        if (
            "firstname" in fields_list or "lastname" in fields_list
        ) and "name" not in fields_list:
            fields_list = list(fields_list) + ["name"]
        result = super(ResUser, self).default_get(fields_list)

        partner_model = self.env["res.partner"]
        inverted = partner_model._get_inverse_name(
            partner_model._get_whitespace_cleaned_name(result.get("name", "")),
            result.get("is_company", False),
        )

        for field in list(inverted.keys()):
            if field in fields_list:
                result[field] = inverted.get(field)

        return result

    @api.onchange("firstname", "lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for rec in self:
            rec.name = rec.partner_id._get_computed_name(rec.lastname, rec.firstname)

    def copy_data(self, default=None):
        """Ensure users are copied right.

        Odoo adds ``(copy)`` to the end of :attr:`~.name` and
        :attr:`~.login`, but the name would get ignored in
        :meth:`~.create` because it also copies explicitly firstname and
        lastname fields.
        """
        default = dict(default or {})
        vals_list = super(ResUser, self).copy_data(default=default)
        partner_model = self.env["res.partner"]
        for user, vals in zip(self, vals_list):
            if "firstname" in default or "lastname" in default:
                # The split fields were given explicitly: they win, and the
                # full name is recomputed from them instead of keeping the
                # "(copy)" name Odoo put in ``vals``.
                firstname = default.get("firstname", user.firstname)
                lastname = default.get("lastname", user.lastname)
                vals["firstname"] = firstname
                vals["lastname"] = lastname
                vals["name"] = partner_model._get_computed_name(lastname, firstname)
            elif default.get("name"):
                # a name given for the copy is split as any typed name is
                vals.update(partner_model._get_inverse_name(default["name"], False))
            elif "name" in vals:
                # Odoo's own "<name> (copy)": keep the split fields and add the
                # suffix to the part that comes last, so multi-word names are
                # not split again (the same rule as for partners).
                firstname = user.firstname or ""
                lastname = user.lastname or ""
                if partner_model._get_names_order() == "first_last":
                    lastname = (
                        self.env._("%s (copy)", lastname)
                        if lastname
                        else self.env._("(copy)")
                    )
                else:
                    firstname = (
                        self.env._("%s (copy)", firstname)
                        if firstname
                        else self.env._("(copy)")
                    )
                vals["firstname"] = firstname or False
                vals["lastname"] = lastname or False
                vals["name"] = partner_model._get_computed_name(lastname, firstname)
        return vals_list
