from odoo import models, fields

class SnSalesCompany(models.Model):
    _inherit = "res.company"

    def wich_logha(self):
       return self.env['ir.config_parameter'].sudo().get_param('sn_sales.print_language')
