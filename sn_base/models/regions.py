from odoo import models, fields

class NtixRegions(models.Model):
    _name = 'sn_base.regions'
    _description = 'Régions et régions'

    code = fields.Char(string="Code", required=True,)
    sequence = fields.Integer(string='Sequence', default=10 )
    name = fields.Char(string='Name', required=True, translate=True)

    _sql_constraints = [
        ('region_uniq', 'unique(code,name)', 'Code and name of region must be unique!'),
    ]


