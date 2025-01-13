from odoo import models, fields

class NticCherifDossierOrg(models.Model):
    _name = "cherif.dossierorg"
    _description = "Dossier Origine"
    _order = 'sequence asc'
    _rec_name = 'name'
    
    sequence = fields.Integer(string='Sequence', default=10 )
    dossier_id = fields.Char('dossier id',required=True)
    name = fields.Char('Name',required=True)
   