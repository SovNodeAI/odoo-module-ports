# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    """Since Odoo 20 a scrap is a ``stock.move`` flagged with ``is_scrap``."""

    _inherit = "stock.move"

    def _action_scrap(self):
        self = self.with_context(validate_analytic=True)
        return super()._action_scrap()
