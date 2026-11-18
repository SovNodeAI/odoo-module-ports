# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

import requests

from odoo.tools import misc


class SignOcaCommon:
    # Tests need to manage templates, requests and fields, as they did when
    # running with an administrator user.
    _test_user_groups = (
        "base.group_user",
        "base.group_partner_manager",
        "mail.group_mail_template_editor",
        "sign_oca.sign_oca_group_admin",
    )

    @classmethod
    def setUpClass(cls):
        cls._super_send = requests.Session.send
        super().setUpClass()
        cls.data = base64.b64encode(
            open(
                misc.file_path(f"{cls.test_module}/tests/empty.pdf"),
                "rb",
            ).read()
        ).decode()
        cls.role_customer = cls.env.ref("sign_oca.sign_role_customer")
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.partner_child = cls.env["res.partner"].create(
            {"name": "Child partner", "parent_id": cls.partner.id}
        )
        # sign_role_supervisor is demo data — create manually in tests
        cls.role_supervisor = cls.env["sign.oca.role"].create(
            {
                "name": "Supervisor",
                "partner_selection_policy": "default",
                "default_partner_id": cls.partner.id,
            }
        )
        cls.role_child_partner = cls.env["sign.oca.role"].create(
            {
                "name": "Child partner",
                "partner_selection_policy": "expression",
                "expression_partner": "{{object.parent_id.id}}",
            }
        )

    @classmethod
    def _request_handler(cls, s, r, /, **kw):
        """Don't block external requests."""
        return cls._super_send(s, r, **kw)
