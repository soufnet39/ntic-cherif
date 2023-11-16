from odoo import models, fields, api

class NticPackaging(models.Model):
    _name = "sn_sales.packaging"
    _description = "Colisages"
    _order = 'sequence'

    name = fields.Char('Nom', required=True)
    sequence = fields.Integer('Sequence', default=1,)
    product_id = fields.Many2one('sn_sales.product', string='Produit')
    qty = fields.Float("Nbr. d'unités")

    # volume = fields.Float('Volume (en m3) ', help="Le volume en m3." )
    # weight = fields.Float('Poids (en kg)', )

    barcode = fields.Char('Barcode', copy=False,)
    product_uom_id = fields.Many2one('sn_sales.uom', related='product_id.uom_sale_id', readonly=True)

    _sql_constraints = [
        ('barcode_uniq_packaging', 'unique(barcode)', "Chaque code a barre doit être assigne a un seul colisage !"),
    ]