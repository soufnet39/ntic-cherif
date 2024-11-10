from odoo import models, fields

class NticCherifDossierOrg(models.Model):
    _name = "cherif.dossierorg"
    _description = "Dossier Origine"
    
    dossier_id = fields.Char('dossier id',required=True)
    name = fields.Char('Name',required=True)
   