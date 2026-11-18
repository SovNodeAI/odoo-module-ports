# Copyright 2024 Tecnativa - David Vidal
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import datetime

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_public_holiday = fields.Boolean(
        string="Public Holiday Today", compute="_compute_is_public_holiday"
    )

    def _compute_is_public_holiday(self):
        holiday_public = self.env["calendar.public.holiday"]
        for item in self:
            # sudo: hr.version - the work address is inherited from the version, which
            # only HR officers can read, while the public holiday flag is read by every
            # internal user (presence icon, avatar card).
            item.is_public_holiday = holiday_public.is_public_holiday(
                fields.Date.context_today(item),
                partner_id=item.sudo().address_id.id,
            )

    def _get_public_holiday_lines(self, date_start, date_end):
        """Just get the employees holidays"""
        domain = self.env["hr.leave"]._get_domain_from_get_unusual_days(
            date_from=date_start, date_to=date_end
        )
        return self.env["calendar.public.holiday.line"].search(domain)

    @api.model
    def get_public_holidays_data(self, date_start, date_end):
        # Include public holidays in the calendar summary
        res = super().get_public_holidays_data(date_start=date_start, date_end=date_end)
        self = self._get_contextual_employee()
        public_holidays = self._get_public_holiday_lines(date_start, date_end).sorted(
            "date"
        )
        res += list(
            map(
                lambda bh: {
                    "id": -bh.id,
                    "colorIndex": 0,
                    "end": (datetime.combine(bh.date, datetime.max.time())).isoformat(),
                    "endType": "datetime",
                    "isAllDay": True,
                    "start": (
                        datetime.combine(bh.date, datetime.min.time())
                    ).isoformat(),
                    "startType": "datetime",
                    "title": bh.name,
                },
                public_holidays,
            )
        )
        return sorted(res, key=lambda x: x["start"])

    def _compute_leave_status(self):
        res = super()._compute_leave_status()
        # Odoo 20 no longer has the "leave_*" IM statuses: the "on leave" display of
        # a user is driven by the ``leave_date_to`` of its employee (see
        # ``hr_holidays/static/src/core/common/im_status_patch.js``). Keep the same
        # behaviour for public holidays by exposing a return date and marking the
        # employee absent.
        for item in self.filtered(lambda x: not x.is_absent and x.is_public_holiday):
            item.is_absent = True
            if item.id:
                today_end = datetime.combine(
                    fields.Date.context_today(item), datetime.max.time()
                )
                back_on = item._get_first_working_interval_batch(
                    {item.id: today_end}
                ).get(item.id)
                item.leave_date_to = (
                    back_on.date() if back_on else fields.Date.context_today(item)
                )
        return res
