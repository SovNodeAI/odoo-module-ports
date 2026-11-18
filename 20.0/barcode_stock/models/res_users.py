# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    # Per-operation-type default filters for the Barcode picking list, kept as a
    # JSON map keyed by operation-type code, e.g.
    #   {"incoming": {"activeFilters": ["date"], "filterValues": {"date": "today"}}}
    # The frontend owns the shape; the server only stores and serves the map so
    # the app can apply a user's starred filter automatically on entry.
    barcode_default_filters = fields.Json(
        default=dict,
        user_writeable=True,
    )
