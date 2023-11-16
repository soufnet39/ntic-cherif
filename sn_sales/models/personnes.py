from odoo import models, fields, api, _

class NticPersonnes(models.Model):
    _name = 'sn_sales.personnes'
    _description = 'Personnes en contact avec les sociétés'

    
    name = fields.Char( string='Nom', required=True )
    fonction =  fields.Char( string='Fonction' )
    phone = fields.Char( string='Phone' )
    email = fields.Char( string='Email' )
    partner_id = fields.Many2one('sn_sales.partner')