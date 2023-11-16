from odoo import models, fields

class SnBaseContentTypes(models.Model):
    _name = 'sn_sales.content_types'
    _rec_name = 'name'
    _description = 'Content Types'

    name = fields.Char('Name' , required=True, Translate=True)
    color = fields.Integer(string='Color Index')
    #taxo_id = fields.Many2one('sn_sales.taxonomies',  copy=True)

