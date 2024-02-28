from odoo import models,api, fields

class NticCherifPriceList(models.Model):
    _inherit = "sn_sales.pricelist"    

    numberOfMonths = fields.Integer('Nombre de mois', default=12)
    
class NticCherifPriceListItem(models.Model):
    _inherit = "sn_sales.pricelist.item"

    price_of_month = fields.Float('Prix du mois') 
   

   

    
