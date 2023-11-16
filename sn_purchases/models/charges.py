from odoo import models, fields, tools,api, _
#from odoo.exceptions import ValidationError, RedirectWarning, UserError


class NticAchatCharges(models.Model):
    _name = "sn_purchases.charges"
    _order = "sequence, name"


    name = fields.Char(string="Charge", required=True, )
    sequence = fields.Integer(string='Priorite', default=10)
    methode_calcule = fields.Selection(string="Methode de calcule", selection=[
        ('amount', 'Montant fixe'), ('percent', 'Pourcentage %'), ], required=False, )
    value_fix = fields.Float(string="Montant Fixe",  required=False, )
    value_percent = fields.Float(string="Pourcentage",  required=False, )

    _sql_constraints = [
        ('cahrge_uniq_name', 'unique(name)', "Chaque charge doit avoir un nom unique !"),
    ]