from odoo import models,api, fields

class NticCherifPriceList(models.Model):
    _inherit = "sn_sales.pricelist"    

    numberOfMonths = fields.Integer('Nombre de mois', default=12)
    
class NticCherifPriceListItem(models.Model):
    _inherit = "sn_sales.pricelist.item"

    price_of_month = fields.Float('Prix du mois') 
    @api.onchange('price_of_month','pricelist_id')
    def _onchange_price_of_month(self):   
        #import wdb; wdb.set_trace()
        if self.price_of_month:
            self.fixed_price = self.price_of_month * self.pricelist_id.numberOfMonths
        else:
            self.fixed_price = 0.0

   

    
