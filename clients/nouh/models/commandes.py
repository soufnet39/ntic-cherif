from odoo import models, fields, api

class NticNouhCommandeLines(models.Model):
    _inherit = 'sn_sales.commande.lines'

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        if not self.product_id:
            return
       
        self.product_id.write({'default_price': self.price_unit,
                               'purchase_price': self.price_unit})
        
