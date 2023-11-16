from odoo import models, fields


class NtixWilayates(models.Model):
    _name = 'sn_base.wilayates'
    _description = "Wilayates of Algeria"

    code = fields.Char(string="Code", required=True,)
    sequence = fields.Integer(string='Sequence', default=10 )
    name = fields.Char(string='Name', required=True, translate=True)
    region_id = fields.Many2one('sn_base.regions', string='Region', required=True)

    _sql_constraints = [
        ('wilaya_uniq', 'unique(code,name)', 'Code et nom de wilaya doit être unique!'),
    ]
