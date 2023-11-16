from odoo import models, fields 

class SnBaseCompany(models.Model):
    _inherit = "res.company"

    wilaya_id = fields.Many2one('sn_base.wilayates',string="Wilaya", required=True)
    mobile = fields.Char(string="Mobile")
    fax = fields.Char(string="fax")
    boite_postale = fields.Char(string="B.P.")
    nis = fields.Char(string="NIS"  )
    rib = fields.Char(string="RIB"  )
    capital_social = fields.Char(string="Capital Social"  )
    m_fisc = fields.Char(string="Mat. Fisc."  )
    a_imp = fields.Char(string="Art. Imp."  )
    reg_com = fields.Char(string="Reg.Com."  )    
