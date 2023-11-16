from odoo import models, fields
class NtixCommunes(models.Model):
    _name = 'sn_base.communes'
    _description = "Communes of Algeria"

    name = fields.Char(string='Name', required=True, translate=True)
    wilaya_id = fields.Many2one('sn_base.wilayates', string='Wilaya')

    _sql_constraints = [
        ('commune_uniq', 'unique(wilaya_id,name)', 'Name of commune must be unique in its wilaya!'),
    ]


