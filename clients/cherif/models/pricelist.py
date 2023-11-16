from odoo import models, fields

class NticCherifPriceList(models.Model):
    _inherit = "sn_sales.pricelist"    

    numberOfMonths = fields.Integer('Nombre de mois', default=12)
    