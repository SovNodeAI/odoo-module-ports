# Copyright 2014-2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import exceptions


class EmptyNamesError(exceptions.ValidationError):
    def __init__(self, record, value=None):
        self.record = record
        self._value = value or record.env._("No name is set.")
        self._name = record.env._("Error(s) with partner %d's name.") % record.id
        self.args = (self._name, self._value)
