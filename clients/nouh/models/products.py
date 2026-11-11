from odoo import models, fields, api


class NticNouhProduct(models.Model):
    _inherit = 'sn_sales.product'
    _description = "Nouh part of product"

    @api.onchange('purchase_price') # change sale price on changing purchase price
    def _onchange_purchase_price(self):
        for record in self:
            record.default_price = record.purchase_price

    @api.onchange('default_price') # change purchase price on changing sale price
    def _onchange_default_price(self):
        for record in self:
            record.purchase_price = record.default_price
    




   
   