from odoo import models, fields, tools

class SnUomCommandes(models.Model):
   _inherit = "sn_sales.commandes"
   show_uom = fields.Boolean(string="Afficher les unités de mesure", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_uom.show_uom'))

class SnUomCommandeLines(models.Model):
   _inherit = "sn_sales.commande.lines"
   product_uom_name = fields.Char(string="Unité", related='product_id.uom_sale_id.name')

   # for purchase module

   product_uom_purchase_name = fields.Char(string="Unité", related='product_id.uom_purchase_id.name')
