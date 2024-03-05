from odoo import models,api, fields

class NticCherifPriceList(models.Model):
    _inherit = "sn_sales.pricelist"    

    numberOfMonths = fields.Integer('Nombre de mois', default=12)
    taux = fields.Integer('Taux %', default=50)

class NticCherifPriceListItem(models.Model):
    _inherit = "sn_sales.pricelist.item"

    price_of_month = fields.Float('Prix du mois') 
    taux = fields.Integer('Taux %', default=50)
        
   

   

    
