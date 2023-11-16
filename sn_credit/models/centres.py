from odoo import models, fields, api, _

class NticCreditCompanyAsWilaya(models.Model):
    _inherit = "res.company"

    # Centres are based on res.company model related to wilaya model    
    code_centre = fields.Char(related='wilaya_id.code')
