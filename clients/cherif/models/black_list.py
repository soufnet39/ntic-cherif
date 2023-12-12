from odoo import models, fields,api
from odoo.exceptions import UserError


class NticCherifBlackList(models.Model):
    _name = "cherif.black_list"    
    _description = "Liste noire des clients"
    _order = 'create_date asc'

    name = fields.Char('Client',required=True)
    ccp_numero = fields.Char(string="CCP",required=True )
    ccp_cle    = fields.Char(string="Clé",required=True)
    wilaya = fields.Char(string="Wilaya",readonly=True)
    user   = fields.Char(string="Agent",readonly=True)

    @api.model
    def create(self, vals):         
        chosen_company_id = self.env.user.company_id    
        vals['wilaya'] = chosen_company_id.wilaya_id.name     
        vals['user'] = self.env.user.name
        return super(NticCherifBlackList, self).create(vals)
            