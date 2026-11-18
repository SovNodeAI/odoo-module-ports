# Copyright (C) 2026  Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.l10n_br_base.tests.tools import load_fixture_files

_logger = logging.getLogger(__name__)


def _ensure_base_user_demo(env):
    """Provide base.user_demo, which only exists with the core demo data."""
    if env.ref("base.user_demo", raise_if_not_found=False):
        return
    user_demo = env["res.users"].create(
        {
            "name": "Demo User",
            "login": "demo",
            "password": "demo",
            "email": "demo@yourcompany.com",
        }
    )
    env["ir.model.data"].create(
        {
            "name": "user_demo",
            "module": "base",
            "res_id": user_demo.id,
            "model": "res.users",
            "noupdate": True,
        }
    )


def _ensure_stock_demo_company(env):
    """Provide stock.res_company_1, which only exists with the stock demo data.

    The module demo data renames that company; when the core demo data is not
    installed, create a stand-in record carrying the same xmlid.
    """
    if env.ref("stock.res_company_1", raise_if_not_found=False):
        return
    partner = env["res.partner"].create(
        {"name": "My Company (Chicago)", "is_company": True, "company_id": False}
    )
    company = env["res.company"].create(
        {
            "name": "My Company (Chicago)",
            "partner_id": partner.id,
            "currency_id": env.ref("base.USD").id,
        }
    )
    env["ir.model.data"].create(
        {
            "name": "res_company_1",
            "module": "stock",
            "res_id": company.id,
            "model": "res.company",
            "noupdate": True,
        }
    )


def load_stock_demo_fixtures(env):
    """Load the demo data the l10n_br_stock hooks work with.

    Since Odoo 19 a new database is installed without demo data unless
    ``--with-demo`` is given, so the demo companies, partners and products
    the module hooks rely on do not exist and the hooks stay inactive. This
    loads the same demo data as fixtures and then runs the module hooks on
    it, so the hooks are still exercised by the tests.
    """
    # base demo partners/users and the Brazilian demo companies
    _ensure_base_user_demo(env)
    load_fixture_files(
        env,
        "l10n_br_base",
        file_names=[
            "l10n_br_base_demo.xml",
            "res_company_demo.xml",
            "res_users_demo.xml",
        ],
    )

    # demo products, made storable by the stock demo data
    load_fixture_files(
        env,
        "product",
        file_names=[
            "data/product_attribute_demo.xml",
            "data/product_category_demo.xml",
            "data/product_demo.xml",
        ],
    )
    load_fixture_files(env, "stock", file_names=["data/stock_demo_pre.xml"])
    _ensure_stock_demo_company(env)

    # emulate a demo installation: the module hooks check these flags
    modules = env["ir.module.module"].search(
        [("name", "in", ("stock", "l10n_br_stock"))]
    )
    modules.demo = True

    from ..hooks import post_init_hook, pre_init_hook

    pre_init_hook(env)
    load_fixture_files(
        env,
        "l10n_br_stock",
        file_names=[
            "res_users_demo.xml",
            "stock_location_demo.xml",
            "res_company_demo.xml",
        ],
    )
    post_init_hook(env)
