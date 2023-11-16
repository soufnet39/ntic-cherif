from odoo import models, fields

class ProductTemplateAttributeLine(models.Model):
    _name = "sn_sales.categories"
    _rec_name = 'taxo_id'
    _description = 'taxonomies Items lines'
    _order = 'taxo_id, id'

    taxo_id = fields.Many2one('sn_sales.taxonomies', string="Taxonomies", ondelete='restrict', required=True, index=True)
    items_ids = fields.Many2many('sn_sales.taxonomies.items', string="Values",domain="[('taxo_id', '=', taxo_id)]")
    product_id= fields.Many2one('sn_sales.product')
    partner_id = fields.Many2one('sn_sales.partner')


class SnSalesTaxonomies(models.Model):
    _name = 'sn_sales.taxonomies'
    _description = 'categories and familly'

    name = fields.Char('Nom', required=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sn_sales.commandes'))
    items = fields.One2many('sn_sales.taxonomies.items', 'taxo_id', string="Items", copy=True,)
    contents = fields.Many2many('sn_sales.content_types', string="Types de contenus", copy=True,)

class SnSalesTaxonomiesItems(models.Model):
    _name = 'sn_sales.taxonomies.items'
    _description = 'items of taxonomies'

    name = fields.Char('Name', required=True)
    taxo_id = fields.Many2one('sn_sales.taxonomies', ondelete='cascade', copy=True, readonly=True)
