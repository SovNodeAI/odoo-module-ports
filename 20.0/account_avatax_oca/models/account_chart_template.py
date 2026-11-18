from odoo import models
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    @template(model="account.tax.group")
    def _get_avatax_tax_group(self, template_code):
        return {"account_avatax_oca.avatax_tax_group": {"name": "AvaTax"}}

    @template(model="account.tax")
    def _get_avatax_tax(self, template_code):
        return {
            "account_avatax_oca.avatax": {
                "name": "AVATAX",
                "description": "Sales Tax",
                "tax_group_id": "account_avatax_oca.avatax_tax_group",
                "amount_type": "percent",
                "amount": 0.0,
                "type_tax_use": "sale",
                "is_avatax": True,
                "country_id": "base.us",
            }
        }

    @template(model="account.fiscal.position")
    def _get_avatax_fiscal_position(self, template_code):
        return {
            "account_avatax_oca.avatax_fiscal_position_us": {
                "name": "Avatax Tax Mapping (US)",
                "is_avatax": True,
                "auto_apply": True,
                "country_id": "base.us",
            }
        }
