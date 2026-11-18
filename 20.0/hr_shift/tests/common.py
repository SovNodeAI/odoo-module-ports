# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestHrShiftBase(BaseCommon):
    # Odoo 20's BaseCommon runs the tests as a dedicated internal user, while the
    # tests were written to run as the admin user (as BaseCommon did up to 19.0).
    _test_user_groups = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company.shift_start_day = "0"
        cls.company.shift_end_day = "4"
        cls.calendar = cls.env["resource.calendar"].create(
            {"name": "Test calendar", "attendance_ids": []}
        )
        for day in range(5):  # From monday to friday
            cls.calendar.attendance_ids = [
                (
                    0,
                    0,
                    {
                        "dayofweek": str(day),
                        "hour_from": "08",
                        "hour_to": "12",
                    },
                ),
                (
                    0,
                    0,
                    {
                        "dayofweek": str(day),
                        "hour_from": "13",
                        "hour_to": "17",
                    },
                ),
            ]
        cls.employee_a = cls.env["hr.employee"].create(
            {
                "name": "Test employee A",
                "company_id": cls.company.id,
                "shift_planning": True,
                "resource_calendar_id": cls.calendar.id,
            }
        )
        cls.employee_b = cls.env["hr.employee"].create(
            {
                "name": "Test employee B",
                "company_id": cls.company.id,
                "shift_planning": True,
                "resource_calendar_id": cls.calendar.id,
            }
        )
        cls.employee_c = cls.env["hr.employee"].create(
            {"name": "Test employee C", "company_id": cls.company.id}
        )
        # Demo data is no longer installed by default in Odoo 20 test databases,
        # so the shift templates the tests rely on are created here with the same
        # values as in demo/demo.xml.
        cls.template_morning = cls.env["hr.shift.template"].create(
            {
                "name": "Morning 8-14",
                "day_of_week_start": "0",
                "day_of_week_end": "4",
                "start_time": 8,
                "end_time": 14,
                "color": 10,
                "tz": "Europe/Brussels",
            }
        )
        cls.template_afternoon = cls.env["hr.shift.template"].create(
            {
                "name": "Afternoon 14-20",
                "day_of_week_start": "0",
                "day_of_week_end": "4",
                "start_time": 14,
                "end_time": 20,
                "color": 4,
                "tz": "Europe/Brussels",
            }
        )
