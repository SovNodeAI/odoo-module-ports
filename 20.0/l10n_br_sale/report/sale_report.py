# Copyright (C) 2011  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models
from odoo.tools import SQL

from odoo.addons.l10n_br_fiscal.constants.fiscal import (
    NFE_IND_PRES,
    NFE_IND_PRES_DEFAULT,
    PRODUCT_FISCAL_TYPE,
)


class SaleReport(models.Model):
    _inherit = "sale.report"

    fiscal_operation_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.operation",
        string="Fiscal Operation",
        readonly=True,
    )

    fiscal_operation_line_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.operation.line",
        string="Fiscal Operation Line",
        readonly=True,
    )

    ind_pres = fields.Selection(
        selection=NFE_IND_PRES,
        string="Buyer Presence",
        default=NFE_IND_PRES_DEFAULT,
    )

    cfop_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.cfop",
        string="CFOP",
    )

    fiscal_type = fields.Selection(
        selection=PRODUCT_FISCAL_TYPE, string="Product Fiscal Type"
    )

    cest_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.cest",
        string="CEST",
    )

    ncm_id = fields.Many2one(comodel_name="l10n_br_fiscal.ncm", string="NCM")

    nbm_id = fields.Many2one(comodel_name="l10n_br_fiscal.nbm", string="NBM")

    icms_value = fields.Float(
        string="ICMS Value",
        digits="Account",
    )

    icmsst_value = fields.Float(
        string="ICMS ST Value",
        digits="Account",
    )

    ipi_value = fields.Float(
        string="IPI Value",
        digits="Account",
    )

    pis_value = fields.Float(
        string="PIS Value",
        digits="Account",
    )

    cofins_value = fields.Float(
        string="COFINS Value",
        digits="Account",
    )

    ii_value = fields.Float(
        string="II Value",
        digits="Account",
    )

    freight_value = fields.Float(
        digits="Account",
    )

    insurance_value = fields.Float(
        digits="Account",
    )

    other_value = fields.Float(
        digits="Account",
    )

    total_with_taxes = fields.Float(
        string="Total with Taxes",
        digits="Account",
    )

    def _select_dict(self, table):
        order_rate = self._case_value_or_one(table.order_id.currency_rate)
        return super()._select_dict(table) | {
            "fiscal_operation_id": table.fiscal_operation_id,
            "fiscal_operation_line_id": table.fiscal_operation_line_id,
            "ind_pres": table.order_id.ind_pres,
            "cfop_id": table.cfop_id,
            "fiscal_type": table.fiscal_type,
            "ncm_id": table.ncm_id,
            "nbm_id": table.nbm_id,
            "cest_id": table.cest_id,
            "icms_value": SQL("SUM(%s)", table.icms_value),
            "icmsst_value": SQL("SUM(%s)", table.icmsst_value),
            "ipi_value": SQL("SUM(%s)", table.ipi_value),
            "pis_value": SQL("SUM(%s)", table.pis_value),
            "cofins_value": SQL("SUM(%s)", table.cofins_value),
            "ii_value": SQL("SUM(%s)", table.ii_value),
            "freight_value": SQL("SUM(%s)", table.freight_value),
            "insurance_value": SQL("SUM(%s)", table.insurance_value),
            "other_value": SQL("SUM(%s)", table.other_value),
            # As in 19.0: price_total divided by the order's currency rate,
            # then the taxes and costs that are not part of price_total.
            "total_with_taxes": SQL(
                "SUM(%s / %s)"
                " + SUM(COALESCE(%s, 0.0))"
                " + SUM(COALESCE(%s, 0.0))"
                " + SUM(COALESCE(%s, 0.0))"
                " + SUM(COALESCE(%s, 0.0))"
                " + SUM(COALESCE(%s, 0.0))",
                table.price_total,
                order_rate,
                table.ipi_value,
                table.icmsst_value,
                table.freight_value,
                table.insurance_value,
                table.other_value,
            ),
        }

    def _groupby_list(self, table):
        return super()._groupby_list(table) + [
            table.fiscal_operation_id,
            table.fiscal_operation_line_id,
            table.order_id.ind_pres,
            table.cfop_id,
            table.fiscal_type,
            table.ncm_id,
            table.nbm_id,
            table.cest_id,
        ]
