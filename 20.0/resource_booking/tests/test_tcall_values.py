# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from freezegun import freeze_time
from lxml.html import fromstring

from odoo.tests import new_test_user, tagged
from odoo.tests.common import HttpCase

from .common import create_test_data


@freeze_time("2021-02-26 09:00:00", tick=True)
@tagged("post_install", "-at_install")
class TCallValuesCase(HttpCase):
    """Values passed to a called template must reach it.

    Since Odoo 20 a ``t-set`` inside the body of a ``t-call`` is rendered
    later, in its own scope, so it no longer feeds the called template. The
    portal templates pass those values as attributes of the ``t-call``
    instead; these tests go through the real HTTP flow to prove it.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_test_data(cls)
        cls.user_portal = new_test_user(
            cls.env,
            login="tcall_ptl",
            password="tcall_ptl",
            groups="base.group_portal",
        )
        cls.user_manager = new_test_user(
            cls.env,
            login="tcall_mgr",
            password="tcall_mgr",
            groups="base.group_user,resource_booking.group_manager",
        )
        cls.booking = cls.env["resource.booking"].create(
            {
                "partner_ids": [(4, cls.user_portal.partner_id.id)],
                "type_id": cls.rbt.id,
            }
        )

    def _url_xml(self, url):
        response = self.url_open(url, timeout=10)
        self.assertEqual(response.status_code, 200)
        return fromstring(response.content)

    def test_portal_my_bookings_breadcrumbs_in_searchbar(self):
        """``breadcrumbs_searchbar`` reaches both portal_layout and the searchbar."""
        self.authenticate("tcall_ptl", "tcall_ptl")
        page = self._url_xml("/my/bookings")
        # The searchbar shows the breadcrumbs instead of a title...
        self.assertTrue(
            page.cssselect(".o_portal_navbar .o_portal_submenu"),
            "portal_searchbar should render the breadcrumbs",
        )
        self.assertFalse(
            page.cssselect(".o_portal_navbar .navbar-brand"),
            "portal_searchbar should not fall back to a title",
        )
        # ...and portal_layout does not render its own breadcrumbs block.
        self.assertFalse(
            page.cssselect(".o_portal.container .o_portal_submenu"),
            "portal_layout should not render a second breadcrumbs block",
        )

    def test_portal_form_fullwidth_alert(self):
        """``o_portal_fullwidth_alert`` and ``backend_url`` reach the callees."""
        self.authenticate("tcall_mgr", "tcall_mgr")
        page = self._url_xml(self.booking.get_portal_url())
        alert = page.cssselect(".alert.alert-info a.alert-link")
        self.assertTrue(alert, "the fullwidth alert should be rendered")
        self.assertIn("/web#return_label=Website", alert[0].get("href"))
        # The chatter container receives the booking as its object.
        discussion = page.cssselect("#discussion")
        self.assertTrue(discussion, "the chatter container should be rendered")
        self.assertEqual(discussion[0].get("data-res_model"), "resource.booking")
        self.assertEqual(discussion[0].get("data-res_id"), str(self.booking.id))

    def test_portal_schedule_fullwidth_alert(self):
        """The scheduling page also gets its fullwidth alert."""
        self.authenticate("tcall_mgr", "tcall_mgr")
        page = self._url_xml(self.booking.get_portal_url(suffix="/schedule"))
        alert = page.cssselect(".alert.alert-info a.alert-link")
        self.assertTrue(alert, "the fullwidth alert should be rendered")
        self.assertIn("/web#return_label=Website", alert[0].get("href"))
        self.assertTrue(page.cssselect(".o_booking_calendar"))
