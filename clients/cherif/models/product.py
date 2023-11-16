from odoo import models, fields,api

class NticCherifProduct(models.Model):
    _inherit = "sn_sales.product"    

    displayed_tags = fields.Text(string='List des prix', compute='_compute_displayed_tags')

    @api.depends('pricelist_item_ids')
    def _compute_displayed_tags(self):
        for record in self:
            tags = record.pricelist_item_ids.mapped('fixed_price')  # Extract 'name' field from related records
            formatted_tags = '  ,  '.join('{:,.2f}'.format(item) for item in tags)  # Join the extracted names
            record.displayed_tags = formatted_tags