from odoo import api, models, fields, _
#from odoo.exceptions import UserError, ValidationError

class SnProductsCategories(models.Model):

    _name = "sn_sales.products_categories"
    _description = "Ntic Products Categories"

    name = fields.Char('Name', index=True, required=True)
    product_id = fields.One2many('sn_sales.product', 'product_categ_id', string='Catégorie')

