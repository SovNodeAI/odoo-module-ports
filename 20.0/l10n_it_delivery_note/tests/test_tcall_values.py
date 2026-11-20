# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import html

from odoo.tests import HttpCase, new_test_user

from .delivery_note_common import StockDeliveryNoteCommon


class TestReportTcallValues(StockDeliveryNoteCommon):
    """In Odoo 20 the body of a t-call is rendered lazily in its own scope, so a
    value set there with t-set no longer reaches the called template. The report
    must pass `address` and `layout_document_title` as attributes of the t-call
    to web.external_layout."""

    def test_report_address_block_and_title(self):
        delivery_note = self.create_delivery_note()
        delivery_note.action_confirm()
        self.assertTrue(delivery_note.name)

        report_html, _report_type = self.env["ir.actions.report"]._render_qweb_html(
            "l10n_it_delivery_note.delivery_note_report_action",
            delivery_note.ids,
        )
        tree = html.fromstring(report_html)

        # web.address_layout renders the address block from the `address` value
        # of the t-call to web.external_layout.
        address_blocks = tree.xpath("//div[@name='address']")
        self.assertTrue(
            address_blocks,
            "the report must render the address block of web.address_layout",
        )
        self.assertIn(self.recipient.name, address_blocks[0].text_content())

        # web.external_layout renders the document title from the
        # `layout_document_title` value of the t-call.
        titles = tree.xpath("//h2[contains(., 'Document:')]")
        self.assertTrue(
            titles,
            "the report must render the document title of web.external_layout",
        )
        self.assertIn(delivery_note.display_name, titles[0].text_content())


class TestPortalTcallValues(StockDeliveryNoteCommon, HttpCase):
    """The portal templates must pass their values as attributes of the t-call:
    `breadcrumbs_searchbar` to portal.portal_layout (otherwise it renders its
    own breadcrumbs next to the searchbar's) and `classes`, `title`, `entries`
    to portal.portal_record_sidebar (otherwise the sidebar is empty)."""

    def setUp(self):
        super().setUp()
        self.portal_user = new_test_user(
            self.env,
            login="portal_tcall",
            password="portal",
            groups="base.group_portal",
        )
        self.portal_user.partner_id = self.recipient
        self.delivery_note = self.create_delivery_note()
        self.delivery_note.action_confirm()

    def test_portal_list_renders_one_breadcrumb(self):
        self.authenticate("portal_tcall", "portal")
        response = self.url_open("/my/delivery-notes")
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)

        # portal.portal_layout renders its own breadcrumbs unless it receives
        # breadcrumbs_searchbar; portal.portal_searchbar renders them when it
        # does. The value must reach both, so the page shows them once.
        breadcrumbs = tree.xpath("//ol[contains(@class, 'o_portal_submenu')]")
        self.assertEqual(
            len(breadcrumbs),
            1,
            "the portal list must render the breadcrumbs once, not twice",
        )

    def test_portal_detail_renders_sidebar(self):
        self.authenticate("portal_tcall", "portal")
        response = self.url_open(f"/my/delivery-notes/{self.delivery_note.id}")
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)

        # portal.portal_record_sidebar renders `title` and `entries`; the
        # download button lives in `entries`.
        sidebar = tree.xpath("//div[contains(@class, 'o_portal_sidebar_content')]")
        self.assertTrue(sidebar, "the portal sidebar must be rendered")
        self.assertTrue(
            sidebar[0].xpath(".//a[contains(@class, 'o_download_btn')]"),
            "the sidebar must render the entries passed to portal_record_sidebar",
        )
        self.assertIn(self.delivery_note.name, sidebar[0].text_content())
