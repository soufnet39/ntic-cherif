from odoo import models, fields

class StockUsers(models.Model):
    _inherit = 'res.users'
    stock_ids = fields.Many2many('sn_stocks.stocks',   string='Stocks under control')
