from odoo import models, fields, tools

class SnUomInvoices(models.Model):
   _inherit = "sn_invoices.invoices"
   show_uom = fields.Boolean(string="Afficher les unités de mesure", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_uom.show_uom'))

class SnUomInvoicesLines(models.Model):
   _inherit = "sn_invoices.invoices.lines"

   product_uom_name = fields.Char(string="Unité", related='product_id.uom_sale_id.name')
