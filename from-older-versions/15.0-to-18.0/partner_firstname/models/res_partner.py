# Copyright 2013 Nicolas Bessi (Camptocamp SA)
# Copyright 2014 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import api, fields, models

from .. import exceptions

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Adds last name and first name; name becomes a stored function field."""

    _inherit = "res.partner"

    firstname = fields.Char("First name", index=True)
    lastname = fields.Char("Last name", index=True)
    name = fields.Char(
        compute="_compute_name",
        inverse="_inverse_name_after_cleaning_whitespace",
        required=False,
        store=True,
        readonly=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Add inverted names at creation if unavailable."""
        created_partners = self.browse()
        for vals in vals_list:
            context = dict(self.env.context)
            name = vals.get("name", context.get("default_name"))
            company_type = vals.get("company_type")
            if company_type:
                is_company = company_type == "company"
            else:
                is_company = vals.get(
                    "is_company", self.default_get(["is_company"])["is_company"]
                )

            if (
                not is_company
                and (vals.get("firstname") or vals.get("lastname"))
                and "name" in vals
            ):
                # The split fields were given explicitly: they win over the
                # full name, which must not be split again on top of them.
                vals.pop("name", None)
                context.pop("default_name", None)
            elif name is not None:
                # Calculate the splitted fields
                inverted = self._get_inverse_name(
                    self._get_whitespace_cleaned_name(name), is_company
                )
                for key, value in inverted.items():
                    if not vals.get(key) or context.get("copy"):
                        vals[key] = value

                # Remove the combined fields
                vals.pop("name", None)
                context.pop("default_name", None)
            # pylint: disable=W8121
            created_partners |= super(
                ResPartner, self.with_context(context)
            ).create([vals])
        return created_partners

    def copy_data(self, default=None):
        """Ensure partners are copied right.

        Odoo adds ``(copy)`` to the end of :attr:`~.name`, but that would get
        ignored in :meth:`~.create` because it also copies explicitly firstname
        and lastname fields.
        """
        default = default or {}
        vals_list = super().copy_data(default=default)
        result = []
        for record, vals in zip(self, vals_list):
            if "company_type" in default:
                is_company = default["company_type"] == "company"
            elif "is_company" in default:
                is_company = default["is_company"]
            else:
                is_company = record.is_company
            if "firstname" in default or "lastname" in default:
                # The split fields were given explicitly: they win, and the
                # full name is recomputed from them.
                vals["name"] = record._get_computed_name(
                    default.get("lastname", record.lastname),
                    default.get("firstname", record.firstname),
                )
            elif default.get("name"):
                vals["name"] = default["name"]
                vals.update(record._get_inverse_name(default["name"], is_company))
            elif is_company:
                name = self.env._("%s (copy)", record.name)
                vals["name"] = name
                vals.update(record._get_inverse_name(name, True))
            else:
                # Keep the split fields and add the suffix to the part that
                # comes last, so multi-word names are not split again.
                firstname = record.firstname or ""
                lastname = record.lastname or ""
                if record._get_names_order() == "first_last":
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
                vals["name"] = record._get_computed_name(lastname, firstname)
            result.append(vals)
        return result

    @api.model
    def default_get(self, fields_list):
        """Invert name when getting default values."""
        if (
            "firstname" in fields_list or "lastname" in fields_list
        ) and "name" not in fields_list:
            fields_list = list(fields_list) + ["name"]
        result = super(ResPartner, self).default_get(fields_list)

        inverted = self._get_inverse_name(
            self._get_whitespace_cleaned_name(result.get("name", "")),
            result.get("is_company", False),
        )

        for field in list(inverted.keys()):
            if field in fields_list:
                result[field] = inverted.get(field)

        return result

    @api.model
    def _names_order_default(self):
        return "first_last"

    @api.model
    def _get_names_order(self):
        """Get names order configuration from system parameters.
        You can override this method to read configuration from language,
        country, company or other"""
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_names_order", self._names_order_default())
        )

    @api.model
    def _get_computed_name(self, lastname, firstname):
        """Compute the 'name' field according to splitted data.
        You can override this method to change the order of lastname and
        firstname the computed name"""
        order = self._get_names_order()
        if order == "last_first_comma":
            return ", ".join(p for p in (lastname, firstname) if p)
        elif order == "first_last":
            return " ".join(p for p in (firstname, lastname) if p)
        else:
            return " ".join(p for p in (lastname, firstname) if p)

    @api.depends("firstname", "lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for record in self:
            record.name = record._get_computed_name(record.lastname, record.firstname)

    def _inverse_name_after_cleaning_whitespace(self):
        """Clean whitespace in :attr:`~.name` and split it.

        The splitting logic is stored separately in :meth:`~._inverse_name`, so
        submodules can extend that method and get whitespace cleaning for free.
        """
        for record in self:
            # Remove unneeded whitespace
            clean = record._get_whitespace_cleaned_name(record.name)
            record.name = clean
            record._inverse_name()

    @api.model
    def _get_whitespace_cleaned_name(self, name, comma=False):
        """Remove redundant whitespace from :param:`name`.

        Removes leading, trailing and duplicated whitespace.
        """
        if isinstance(name, bytes):
            # With users coming from LDAP, name can be a byte encoded string.
            # This happens with FreeIPA for instance.
            name = name.decode("utf-8")

        try:
            name = " ".join(name.split()) if name else name
        except UnicodeDecodeError:
            # with users coming from LDAP, name can be a str encoded as utf-8
            # this happens with ActiveDirectory for instance, and in that case
            # we get a UnicodeDecodeError during the automatic ASCII -> Unicode
            # conversion that Python does for us.
            # In that case we need to manually decode the string to get a
            # proper unicode string.
            name = " ".join(name.decode("utf-8").split()) if name else name

        if comma:
            name = name.replace(" ,", ",")
            name = name.replace(", ", ",")
        return name

    @api.model
    def _get_inverse_name(self, name, is_company=False):
        """Compute the inverted name.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.

        This method can be easily overriden by other submodules.
        You can also override this method to change the order of name's
        attributes

        When this method is called, :attr:`~.name` already has unified and
        trimmed whitespace.
        """
        # Company name goes to the lastname
        if is_company or not name:
            parts = [name or False, False]
        # Guess name splitting
        else:
            order = self._get_names_order()
            # Remove redundant spaces
            name = self._get_whitespace_cleaned_name(
                name, comma=(order == "last_first_comma")
            )
            parts = name.split("," if order == "last_first_comma" else " ", 1)
            if len(parts) > 1:
                if order == "first_last":
                    parts = [" ".join(parts[1:]), parts[0]]
                else:
                    parts = [parts[0], " ".join(parts[1:])]
            else:
                while len(parts) < 2:
                    parts.append(False)
        return {"lastname": parts[0], "firstname": parts[1]}

    def _inverse_name(self):
        """Try to revert the effect of :meth:`._compute_name`."""
        for record in self:
            parts = record._get_inverse_name(record.name, record.is_company)
            record.lastname = parts["lastname"]
            record.firstname = parts["firstname"]

    @api.constrains("firstname", "lastname")
    def _check_name(self):
        """Ensure at least one name is set."""
        for record in self:
            if all(
                (
                    record.type == "contact" or record.is_company,
                    not (record.firstname or record.lastname),
                )
            ):
                raise exceptions.EmptyNamesError(record)

    @api.model
    def _install_partner_firstname(self):
        """Save names correctly in the database.

        Before installing the module, field ``name`` contains all full names.
        When installing it, this method parses those names and saves them
        correctly into the database. This can be called later too if needed.
        """
        # Find records with empty firstname and lastname
        records = self.search([("firstname", "=", False), ("lastname", "=", False)])

        # Force calculations there
        records._inverse_name()
        _logger.info("%d partners updated installing module.", len(records))

    # Disabling SQL constraint givint a more explicit error using a Python
    # contstraint
    _sql_constraints = [("check_name", "CHECK( 1=1 )", "Contacts require a name.")]
