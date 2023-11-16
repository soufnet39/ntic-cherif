# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, registry, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class StockRule(models.Model):
    """ A rule describe what a procurement should do; produce, buy, move, ... """
    _name = 'sn_stocks.rules'
    _description = "Regle d'approvisionnemt des Stocks"
    _order = "sequence, id"

    name = fields.Char('Name', required=True, translate=True,)
    active = fields.Boolean('Active', default=True,)
    action = fields.Selection(
        selection=[('pull', 'Pull From'), ('push', 'Push To'), ('pull_push', 'Pull & Push')], string='Action',
        required=True)
    sequence = fields.Integer('Sequence', default=20)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)
    stock_source_id = fields.Many2one('stock.location', 'Stock Source', required=True)
    location_destination_id = fields.Many2one('sn_stocks.stocks', 'Stock Destination')
    delay = fields.Integer('Delay', default=0, help="The expected date of the created transfer will be computed based on this delay.")
    partner_address_id = fields.Many2one('sn_sales.partner', 'Partner Address', help="Address where goods should be delivered. Optional.")
    auto = fields.Selection([
        ('manual', 'Opération Manuelle'),
        ('transparent', 'Opération Automatique')], string='Automatic Move',
        default='manual', index=True, required=True,  )


    def _get_message_values(self):
        """ Return the source, destination and picking_type applied on a stock
        rule. The purpose of this function is to avoid code duplication in
        _get_message_dict functions since it often requires those data.
        """
        source = self.location_src_id and self.location_src_id.display_name or _('Source Location')
        destination = self.location_id and self.location_id.display_name or _('Destination Location')
        operation = self.picking_type_id and self.picking_type_id.name or _('Opération Type')
        return source, destination, operation



