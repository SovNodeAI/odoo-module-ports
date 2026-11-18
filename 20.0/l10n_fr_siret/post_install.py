# Copyright 2021-2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import logging

from stdnum.eu.vat import is_valid as vat_is_valid
from stdnum.fr.siren import is_valid as siren_is_valid
from stdnum.fr.siret import is_valid as siret_is_valid

from odoo.fields import Domain

logger = logging.getLogger(__name__)

FR_SIRET_KEY = "FR_SIRET"
FR_SIREN_KEY = "FR_SIREN"


def _get_company_registry(partner):
    identifiers = partner.additional_identifiers or {}
    for key in (FR_SIRET_KEY, FR_SIREN_KEY):
        value = identifiers.get(key)
        if value:
            return "".join(x for x in value if not x.isspace())
    return False


def clean_bad_siren_siret(env):
    logger.info("Starting validity/consistency check of siret/siren on res.partner")
    fr_country_codes = env["res.company"]._get_france_country_codes()
    domain = Domain(
        [
            ("additional_identifiers", "!=", False),
            ("country_id", "in", fr_country_codes),
            ("is_company", "=", True),
            ("parent_id", "=", False),
        ]
    )
    partners = env["res.partner"].with_context(active_test=False).search(domain)
    for partner in partners:
        company_registry = _get_company_registry(partner)
        if company_registry:
            siren_from_vat = False
            siren = False
            chatter_msg = False
            if (
                partner.vat
                and partner.vat.startswith("FR")
                and vat_is_valid(partner.vat)
                and siren_is_valid(partner.vat[4:])
            ):
                siren_from_vat = partner.vat[4:]
            if len(company_registry) == 14 and siret_is_valid(company_registry):
                siren = company_registry[:9]
                assert siren_is_valid(siren)
            elif len(company_registry) == 9 and siren_is_valid(company_registry):
                siren = company_registry
            elif len(company_registry) > 9 and siren_is_valid(company_registry[:9]):
                new_company_registry = company_registry[:9]
                siren = new_company_registry
                chatter_msg = env._(
                    "Initial SIRET '%(company_registry)s' was invalid, "
                    "but the 9 first digits was a valid SIREN, "
                    "so the value was updated to '%(siren)s'.",
                    company_registry=company_registry,
                    siren=siren,
                )
            else:
                new_company_registry = False
                chatter_msg = env._(
                    "Initial SIRET '%(company_registry)s' was invalid, "
                    "so the value has been removed.",
                    company_registry=company_registry,
                )
            if siren_from_vat and siren and siren_from_vat != siren:
                new_company_registry = False
                chatter_msg = env._(
                    "SIRET '%(company_registry)s' has been removed because "
                    "it is not consistent with VAT '%(vat)s'.",
                    company_registry=company_registry,
                    vat=partner.vat,
                )
            if chatter_msg:
                identifiers = dict(partner.additional_identifiers or {})
                identifiers.pop(FR_SIRET_KEY, None)
                identifiers.pop(FR_SIREN_KEY, None)
                if new_company_registry:
                    key = (
                        FR_SIRET_KEY
                        if len(new_company_registry) == 14
                        else FR_SIREN_KEY
                    )
                    identifiers[key] = new_company_registry
                partner.write({"additional_identifiers": identifiers or False})
                partner.message_post(body=chatter_msg)

    logger.info("End validity/consistency check of siret/siren on res.partner")
