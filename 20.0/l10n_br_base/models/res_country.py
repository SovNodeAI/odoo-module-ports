# Copyright (C) 2009  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class Country(models.Model):
    _inherit = "res.country"

    bc_code = fields.Char(
        string="BC Code",
        size=4,
    )

    ibge_code = fields.Char(
        string="IBGE Code",
        size=4,
    )

    siscomex_code = fields.Char(
        # Odoo 20 enforces the size in the database column; the SISCOMEX
        # codes of Myanmar (0930) and Slovakia (2470) have four digits.
        size=4,
    )

    nationality_code = fields.Char(
        size=2,
    )
