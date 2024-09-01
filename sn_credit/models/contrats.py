from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import string

class NticContrats(models.Model):
    _name = "sn_credit.contrats"
    _description = "type de contrats de vente en credit"

    name = fields.Char(string='Réference', required=True, copy=False, index=True, default='', )
    description = fields.Char(string="Déscription", required=False, )
    jour_retrait = fields.Integer(string="Jour de retrait", required=True, default=10 )
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company.id)
    nbr_months=fields.Integer(string='Nombre de mois proposé',default=12)
    nbr_aksats=fields.Integer(string='Nombre aksats',default=1)
    users_ids = fields.Many2many(
        string='Users',
        comodel_name='res.users' ,domain="[('is_company', '=', False)]"  )
    ccp_numero =  fields.Char('Numéro CCP', )
    ccp_cle =  fields.Char('Clé CCP', )
    comp_name = fields.Char('Nom Société')
    comp_address = fields.Char('Adresse')
    comp_phone = fields.Char('Numéro télephone')

    _sql_constraints = [
        ('contrat_uniq', 'unique(name,company_id)', 'Le nom du contrat doit être unique dans le même centre!'),
    ]

    @api.constrains('name','jour_retrait')
    def _check_values(self):
        if len(self.name)>1 or self.name not in string.ascii_uppercase:
            raise Warning(_('Le nom doit être une lettre en majuscule,de A à Z.'))
        if self.jour_retrait<1 or self.jour_retrait>31:
            raise Warning(_('Le Jour doit être entre 1 et 31'))
