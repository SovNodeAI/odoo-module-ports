#    Copyright (C) 2016 MultidadosTI (http://www.multidadosti.com.br)
#    @author Michell Stuttgart <michellstut@gmail.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResBank(models.Model):
    # Odoo 20 removed ``res.bank``: its data was flattened into
    # ``res.partner.bank``.  The Brazilian CNAB payment order logic still needs
    # a bank directory (COMPE code, short name, ISPB number) that payment
    # modes, CNAB codes and bank journals can point to, so a minimal ``res.bank``
    # is provided here.
    _name = "res.bank"
    _description = "Bank"
    _order = "name, id"
    _rec_names_search = ["name", "bic"]

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    bic = fields.Char(
        "Bank Identifier Code",
        index=True,
        help="Sometimes called BIC or Swift.",
    )
    country_id = fields.Many2one("res.country", string="Country")

    short_name = fields.Char()

    code_bc = fields.Char(
        string="Brazilian Bank Code",
        size=3,
        help="Brazilian Bank Code ex.: 001 is the code of Banco do Brasil",
    )

    ispb_number = fields.Char(
        string="ISPB Number",
        size=8,
    )

    compe_member = fields.Boolean(
        string="COMPE Member",
        default=False,
    )

    @api.depends("name", "bic")
    def _compute_display_name(self):
        for bank in self:
            name = (bank.name or "") + (bank.bic and (" - " + bank.bic) or "")
            bank.display_name = name

    @api.model
    def _search_display_name(self, operator, value):
        if operator in ("ilike", "not ilike") and value:
            domain = ["|", ("bic", "=ilike", value + "%"), ("name", "ilike", value)]
            if operator == "not ilike":
                domain = ["!", *domain]
            return domain
        return super()._search_display_name(operator, value)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("bic", False):
                vals["bic"] = vals["bic"].upper()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("bic", False):
            vals["bic"] = vals["bic"].upper()
        return super().write(vals)
