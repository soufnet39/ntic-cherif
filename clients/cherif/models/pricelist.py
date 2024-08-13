from odoo import models,api, fields

class NticCherifPriceList(models.Model):
    _inherit = "sn_sales.pricelist"    

    numberOfMonths = fields.Integer('Nombre de mois', default=12)
    taux = fields.Integer('Taux %', default=50)

class NticCherifPriceListItem(models.Model):
    _inherit = "sn_sales.pricelist.item"

    price_of_month = fields.Float('Prix du mois') 
    taux = fields.Integer('Taux %', default=50)
    def calcul_price(self):
        self.fixed_price = self.price_of_month * self.pricelist_id.numberOfMonths

    def calcul_price_on_ref(self):
        parent_price_unit_value = self.env.context.get('parent_price_unit')
        
        self.fixed_price = parent_price_unit_value*(1+self.taux/100)
        self.price_of_month = self.fixed_price/self.pricelist_id.numberOfMonths
