from odoo import models, fields, api
from odoo.exceptions import UserError

class StocksQuantities(models.Model):
    _name = "sn_stocks.quantities"

    product_id = fields.Many2one('sn_sales.product', string='Product', required=True,   change_default=True, ondelete='restrict')