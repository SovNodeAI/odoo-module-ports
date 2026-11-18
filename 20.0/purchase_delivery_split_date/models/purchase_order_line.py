# Copyright 2014-2016 Numérigraphe SARL
# Copyright 2017 ForgeFlow, S.L.
# Copyright 2021 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timezone
from zoneinfo import ZoneInfo

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _purchase_split_date_get_group_keys(self, picking):
        """Define the key that will be used to group.

        The key should be defined as a tuple of dictionaries, with each element
        containing a dictionary element with the field that you want to group
        by. This method is designed for extensibility, so that other modules
        can add additional keys or replace them by others.
        """
        tz = self.order_id.picking_type_id.warehouse_id.partner_id.tz
        wh_tz = ZoneInfo(tz) if tz else self.env.tz
        date_planned_tz = self.date_planned.astimezone(timezone.utc).astimezone(wh_tz)
        date = date_planned_tz.date()
        # Split date value to obtain only the attributes year, month and day
        key = (("date_planned", date),)
        return key

    def _purchase_split_date_get_sorted_keys(self):
        """Return a tuple of keys to use in order to sort the order lines.

        This method is designed for extensibility, so that other modules can
        add additional keys or replace them by others.
        """
        return (self.date_planned,)

    def _create_stock_moves(self, picking=False):
        """Group the receptions in one picking per expected date."""
        if picking:
            return super()._create_stock_moves(picking)
        other_lines = self.filtered("display_type") | self.filtered(
            lambda line: line.product_id.type != "consu"
        )
        moves = super(PurchaseOrderLine, self - other_lines)._create_stock_moves()
        if moves:
            moves_typed = moves.with_context(purchase_delivery_split_date=True)
            for group_moves in moves_typed.grouped(
                lambda move: move.purchase_line_id._purchase_split_date_get_group_keys(
                    picking
                )
            ).values():
                group_moves._assign_picking()
        return moves | super(PurchaseOrderLine, other_lines)._create_stock_moves()

    def _update_move_dates(self, date_planned=False, date_promised=False):
        """Update both move fields so a planned-date change splits pickings."""
        moves_to_update = self.move_ids.filtered(lambda m: m.state not in ('done', 'cancel'))
        if not moves_to_update:
            moves_to_update = self.move_dest_ids.filtered(lambda m: m.state not in ('done', 'cancel'))
        if date_planned:
            moves_to_update.write({'date_deadline': date_planned})
        return super()._update_move_dates(date_planned, date_promised)

    def _compute_price_unit_and_date_planned_and_name(self):
        """
        If the line product quantity is changed and a seller is found,
        the date_planned is updated from the supplier (in _get_date_planned())
        """
        date_planned_by_record = dict()
        for line in self:
            date_planned_by_record[line.id] = line.date_planned
        res = super()._compute_price_unit_and_date_planned_and_name()
        for line in self:
            if (
                date_planned_by_record[line.id]
                and line.date_planned <= date_planned_by_record[line.id]
            ):
                line.date_planned = date_planned_by_record[line.id]
        return res
