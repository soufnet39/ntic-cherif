from odoo import models, fields, tools

class SnUomProduct(models.Model):
    _inherit = "sn_sales.product"

    uom_sale_id = fields.Many2one('sn_uom.uom', 'Unité de Mesure Vente',  help="Unité de mesure de vente par defaut.")
    uom_purchase_id = fields.Many2one('sn_uom.uom', 'Unité de Mesure Achat', help="Unité de mesure d'achat par defaut.")
