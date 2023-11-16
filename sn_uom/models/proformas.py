from odoo import models, fields, tools

class SnUomProformas(models.Model):
   _inherit = "sn_sales.proformas"

   show_uom = fields.Boolean(string="Afficher les unités de mesure", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_uom.show_uom'))



class SnUomProformaLines(models.Model):
   _inherit = "sn_sales.proforma.lines"

   product_uom_name = fields.Char(string="Unité", related='product_id.uom_sale_id.name')
