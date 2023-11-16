from odoo import models, fields, api, _
from odoo.exceptions import UserError

class NticCherifCommande(models.Model):
    _inherit = "sn_sales.partner"
    
    date_naissance = fields.Date(string='Date de naissance', copy=False)
    lieu_naissance = fields.Char(string="Lieu de naissance")
    pere = fields.Char(string="Nom du père")
    mere = fields.Char(string="Nom de la mère")
    nom_epous = fields.Char(string="Nom Epous")

    # function:     // exist already
    employeur = fields.Char(string="Employeur")
    identity_card_number = fields.Char(string="Pièce d'identité n°")
    identity_card_date = fields.Date(string="PI délivré le")
    identity_card_place = fields.Char(string="PI délivré à")

