from odoo import api, fields, models, _


    
class wiz_selected_products(models.TransientModel):

    _name = 'cherif.impressionprix'

    product_name = fields.Char("product" )
    prices_ids = fields.One2many('cherif.impressionprix.detail', 'product_id', 'Pricelist Items')
    

    @api.model
    def default_get(self, fields_list):
        defaults = super(wiz_selected_products, self).default_get(fields_list)
        
        prd_ids = self._context.get('active_model') == 'sn_credit.wiz_rest_product' and self._context.get('active_ids') or []
        if prd_ids:
            prd = self.env['sn_sales.product'].browse(prd_ids[0])
            if prd:
                defaults['product_name'] = prd.name                
                detail_lines = []
            
                for pricelist_item in prd.pricelist_item_ids:
                    detail_lines.append((0, 0, {
                        'name': pricelist_item.pricelist_id.name,
                        'numberOfMonths': pricelist_item.pricelist_id.numberOfMonths,
                        'prix': pricelist_item.fixed_price,
                        'price_of_month': pricelist_item.price_of_month,
                    }))
            
            defaults['prices_ids'] = detail_lines

        
        return defaults
    
class wiz_selected_products_detail(models.TransientModel):

    _name = 'cherif.impressionprix.detail'

    product_id = fields.Many2one('cherif.impressionprix')
    product_name = fields.Char(related='product_id.product_name')
    name= fields.Char('name')
    numberOfMonths= fields.Integer('Mois')
    prix = fields.Float('Prix Global')
    price_of_month = fields.Float('Prix par mois')

    def print_line(self):
        return self.env.ref('cherif.product_monthly_price_report').report_action(self)
