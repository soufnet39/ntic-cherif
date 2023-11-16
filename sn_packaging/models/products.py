
from odoo import models, fields, tools, api

class SnPackagingProducts(models.Model):
    _inherit = "sn_sales.product"

    volume = fields.Float('Volume (en m3) ', help="Le volume en m3." ,
                            digits="3 Zeros",
                            default=0.0)
    weight = fields.Float('Poids (en kg)',
                            digits="3 Zeros",
                            default=0.0,
        help="Ppoids du produit, emballage non inclus. L'unite de mesure est le kg")

    # product_colisage = fields.Many2one('sn_sales.packaging',  string='Colisage', ) # domain=[('product_id','=',-1)]

    # packaging_ids = fields.One2many(
    #     'sn_sales.packaging', 'product_id', 'Product Packages',
    #     help="Gives the different ways to package the same product.")

