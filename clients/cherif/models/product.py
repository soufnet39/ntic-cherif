from odoo import models, fields,api

class NticCherifProduct(models.Model):
    _inherit = "sn_sales.product"    

    displayed_tags = fields.Text(string='List des prix', compute='_compute_displayed_tags')

    @api.depends('pricelist_item_ids')
    def _compute_displayed_tags(self):
        for record in self:
            tags = record.pricelist_item_ids.mapped(lambda r:'{1:,.2f}:[{0:.0f}]'.format(r.pricelist_id.numberOfMonths,r.fixed_price))  
            formatted_tags = '  ,  '.join(tags)  # Join the extracted names
            record.displayed_tags = formatted_tags

   