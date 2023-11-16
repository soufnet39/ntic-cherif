# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class Pricelist(models.Model):
    _name = "sn_sales.pricelist"
    _description = "Pricelist"
    _order = "sequence asc, id desc"
  
    def _get_default_item_ids(self):
        ProductPricelistItem = self.env['sn_sales.pricelist.item']
        vals = ProductPricelistItem.default_get(list(ProductPricelistItem._fields))
        return [[0, False, vals]]

    name = fields.Char('Libellé', required=True, translate=True)
    active = fields.Boolean('Active', default=True)
    item_ids = fields.One2many('sn_sales.pricelist.item', 'pricelist_id', 'Pricelist Items',  copy=True, default=_get_default_item_ids)

    # must be declared in security part
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sn_sales.pricelist'))
   
    sequence = fields.Integer(default=10)
    # region_ids = fields.Many2many('sn_base.regions', 'region_pricelist_rel', 'pricelist_id', 'sn_base_regions_id', string='Regions')



class PricelistItem(models.Model):
    _name = "sn_sales.pricelist.item"
    _description = "Pricelist Item"
    _order = "id desc"


    pricelist_id = fields.Many2one('sn_sales.pricelist', 'Libellé de prix', index=True, ondelete='cascade')
    product_id = fields.Many2one(
         'sn_sales.product', 'Product', ondelete='cascade',
          help="Specify a product. Keep empty otherwise.")
    min_quantity = fields.Integer('Min. Quantity', default=0,)    
    fixed_price = fields.Float('Prix', )