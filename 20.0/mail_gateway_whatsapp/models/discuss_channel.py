# Copyright 2024 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools import BinaryBytes
from odoo.tools.misc import file_path

from odoo.addons.base.models.avatar_mixin import get_random_ui_color_from_seed


class DiscussChannel(models.Model):
    _inherit = "discuss.channel"

    def _generate_avatar(self):
        if self.gateway_id.gateway_type == "whatsapp":
            avatar = self._generate_avatar_gateway()
            if not avatar:
                return False
            return BinaryBytes(avatar.encode())
        return super()._generate_avatar()

    def _generate_avatar_gateway(self):
        if self.gateway_id.gateway_type == "whatsapp":
            path = file_path("mail_gateway_whatsapp/static/description/icon.svg")
            with open(path) as f:
                avatar = f.read()

            bgcolor = get_random_ui_color_from_seed(self.uuid)
            avatar = avatar.replace("fill:#875a7b", f"fill:{bgcolor}")
            return avatar
        return super()._generate_avatar_gateway()
