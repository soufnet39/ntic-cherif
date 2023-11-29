from odoo import models, api, _ 

class NticCreditProduct(models.Model):
    _inherit = "sn_sales.product"
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):

        args = args or []
        recs = self.browse()
        names = name.split(' ')
        names_condition = [ ('name', 'ilike', n) for n in names ]
        if name:
            recs = self.search((args + names_condition),limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()