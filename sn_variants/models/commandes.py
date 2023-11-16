
from odoo import api, fields, models,_

class NticSaleCommandeLines(models.Model):
    _inherit = 'sn_sales.commande.lines'
    _parent_name = "parent_id"
    _parent_store = True

    parent_id = fields.Many2one('sn_sales.commande.lines', 'Parent', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('sn_sales.commande.lines', 'parent_id', 'item of composition')
