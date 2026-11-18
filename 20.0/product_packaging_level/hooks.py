# Copyright 2022 ACSONE SA/NV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade

from odoo import SUPERUSER_ID, api


def pre_init_hook(env):
    if openupgrade.table_exists(env.cr, "product_packaging_type"):
        env = api.Environment(env.cr, SUPERUSER_ID, {})
        # Former version of the module is present
        models = [("product.packaging.type", "product.packaging.level")]
        openupgrade.rename_models(env.cr, models)
        fields = [
            (
                "product.packaging",
                "product_packaging",
                "packaging_type_id",
                "packaging_level_id",
            )
        ]
        openupgrade.rename_fields(env, fields, no_deep=True)

        modules = [("product_packaging_type", "product_packaging_level")]
        openupgrade.update_module_names(env.cr, modules, merge_modules=True)

    env.cr.execute(
        """
        CREATE TABLE IF NOT EXISTS product_packaging_level (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            code VARCHAR NOT NULL,
            sequence INTEGER NOT NULL,
            has_gtin BOOLEAN,
            active BOOLEAN,
            is_default BOOLEAN,
            default_lang_id INTEGER REFERENCES res_lang(id),
            name_policy VARCHAR NOT NULL,
            create_uid INTEGER REFERENCES res_users(id),
            create_date TIMESTAMP,
            write_uid INTEGER REFERENCES res_users(id),
            write_date TIMESTAMP
        )
        """
    )
    env.cr.execute(
        """
        INSERT INTO product_packaging_level
            (name, code, sequence, active, is_default, default_lang_id, name_policy)
        SELECT 'Default Level', 'DEFAULT', 1, TRUE, TRUE, id, 'by_package_level'
        FROM res_lang
        WHERE active
        ORDER BY id
        LIMIT 1
        ON CONFLICT DO NOTHING
        """
    )
    env.cr.execute(
        """
        INSERT INTO ir_model_data
            (module, name, model, res_id, noupdate, create_uid, create_date, write_uid, write_date)
        SELECT 'product_packaging_level', 'product_packaging_level_default',
            'product.packaging.level', id, FALSE, 1, NOW(), 1, NOW()
        FROM product_packaging_level
        WHERE is_default
        LIMIT 1
        ON CONFLICT DO NOTHING
        """
    )
    env.cr.execute("ALTER TABLE uom_uom ADD COLUMN IF NOT EXISTS packaging_level_id INTEGER")
    env.cr.execute(
        """
        UPDATE uom_uom
        SET packaging_level_id = (
            SELECT id FROM product_packaging_level WHERE is_default LIMIT 1
        )
        WHERE packaging_level_id IS NULL
        """
    )

    if openupgrade.table_exists(env.cr, "product_packaging"):
        env.cr.execute(
            """
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'product_packaging'
            """
        )
        columns = {row[0] for row in env.cr.fetchall()}
        expressions = {
            "name": "pack.name",
            "relative_factor": "COALESCE(pack.qty, 1)",
            "sequence": "pack.sequence",
            "active": "COALESCE(pack.active, TRUE)",
            "package_type_id": "pack.package_type_id",
            "packaging_level_id": "pack.packaging_level_id",
            "create_uid": "pack.create_uid",
            "create_date": "pack.create_date",
            "write_uid": "pack.write_uid",
            "write_date": "pack.write_date",
        }
        selected = [
            expressions[column] if column in columns else "NULL"
            for column in expressions
        ]
        if "product_id" in columns:
            products = "JOIN product_product AS product ON product.id = pack.product_id"
        else:
            products = (
                "CROSS JOIN LATERAL (SELECT uom_id AS relative_uom_id "
                "FROM product_template LIMIT 1) AS product"
            )
        env.cr.execute(
            f"""
            INSERT INTO uom_uom
                (name, relative_factor, relative_uom_id, sequence, active,
                 package_type_id, packaging_level_id,
                 create_uid, create_date, write_uid, write_date)
            SELECT {', '.join(selected[:2])},
                product.relative_uom_id,
                {', '.join(selected[2:])}
            FROM product_packaging AS pack
            {products}
            """
        )
        env.cr.execute("UPDATE uom_uom SET parent_path = concat(id, '/')")
        env.cr.execute(
            """
            INSERT INTO product_template_uom_uom_rel (product_template_id, uom_uom_id)
            SELECT product.product_tmpl_id, uom.id
            FROM product_packaging AS pack
            JOIN product_product AS product ON product.id = pack.product_id
            JOIN uom_uom AS uom ON uom.relative_uom_id = product.uom_id
                AND uom.relative_factor = pack.qty
                AND uom.package_type_id IS NOT DISTINCT FROM pack.package_type_id
            """
            if "product_id" in columns
            else """
            INSERT INTO product_template_uom_uom_rel (product_template_id, uom_uom_id)
            SELECT product.id, uom.id
            FROM product_packaging AS pack
            CROSS JOIN LATERAL (
                SELECT product.id
                FROM product_template AS product
                WHERE product.active
                ORDER BY product.id
                LIMIT 1
            ) AS product
            JOIN uom_uom AS uom ON uom.relative_factor = pack.qty
                AND uom.package_type_id IS NOT DISTINCT FROM pack.package_type_id
            """
        )

