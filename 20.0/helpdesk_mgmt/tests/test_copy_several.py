# Copyright 2026 SovNode AI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import TestHelpdeskTicketBase


class TestCopySeveral(TestHelpdeskTicketBase):
    def test_duplicate_two_tickets_from_the_list(self):
        """Duplicate with two rows selected in the list view.

        Since 18.0 the web client copies every selected record in one call.
        """
        tickets = self.ticket_a_unassigned | self.ticket_a_user_own
        copies = tickets.copy()
        self.assertEqual(len(copies), 2)
        numbers = set(copies.mapped("number"))
        self.assertEqual(len(numbers), 2)
        self.assertFalse(numbers & set(tickets.mapped("number")))
