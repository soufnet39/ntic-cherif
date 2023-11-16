from odoo import fields, models

class ProductVariantes(models.Model):
    _name = "sn_variants.categories"
    _rec_name = 'variant_id'
    _description = 'variants Items lines'
    _order = "sequence, id"

  
    sequence = fields.Integer(string='Sequence', default=10)
    variant_id = fields.Many2one('sn_variants.variants', string="variants", ondelete='restrict', required=True, index=True)
    items_ids = fields.Many2many('sn_variants.variants.items', string="Values", domain="[('variant_id', '=', variant_id)]")
    product_id = fields.Many2one('sn_sales.product')
    
class SnVariantsVariants(models.Model):
    _name = 'sn_variants.variants'
    _description = 'categories and familly'
    _order = "sequence, id"

    name = fields.Char('Nom', required=True)
    sequence = fields.Integer(string='Sequence', default=10)

    #company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sn_sales.commandes'))
    items = fields.One2many('sn_variants.variants.items', 'variant_id', string="Items", copy=True,)
    unity = fields.Selection(
        string='Unité',
        selection=[('unit', 'Unité'), ('ml', 'ML'),('m2', 'M2'), ('m3', 'M3')] )
    display_type = fields.Selection(
        string='Display Type',
        selection=[('radio', 'Radio'), ('select', 'Selection'),('color', 'couleur')] )
   
class SnVariantsVariantsItems(models.Model):
    _name = 'sn_variants.variants.items'
    _description = 'items of variants'

    name = fields.Char('Name', required=True)
    item_abrv = fields.Char("Abréviation",required=True)
    variant_id = fields.Many2one('sn_variants.variants', ondelete='cascade', copy=True, readonly=True)
    html_color = fields.Char('Color')

    _sql_constraints = [
        ('abrv_distinct',
         'unique(item_abrv,variant_id)',
         'Abréviation must be unique in then category.'),
    ]


