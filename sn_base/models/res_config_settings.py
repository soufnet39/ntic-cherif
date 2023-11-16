from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, Warning


class SNbaseSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    # @api.model
    # def _get_default_wilaya(self):
    #     # if self.company_wilaya_id==0:
    #     #w_id = int(self.env['ir.config_parameter'].sudo().get_param("sn_base.company_wilaya_id"))
    #     res = {}
    #     w_id=self.company_wilaya_id
    #     if w_id>0:
    #         res=  self.env['sn_base.wilayates'].search([('id','=',w_id)])
    #     return res


    company_places = fields.Selection(string="places commerciaux",
                                 selection=[
                                     ('mono', 'Mono place'),
                                     ('multi', 'Multi places'),
                                 ], default='mono',
                                )

    wilayates = fields.Many2one(comodel_name="sn_base.wilayates", string="Wilaya",) # default= _get_default_wilaya
    company_wilaya_id = fields.Integer(string="Wilaya",  )

    @api.onchange('wilayates')
    def _onchange_uom(self):
        if self.wilayates.id:
            self.company_wilaya_id = self.wilayates.id

    def get_values(self):
        res=super(SNbaseSettings, self).get_values()
        res.update(company_places = self.env['ir.config_parameter'].sudo().get_param("sn_base.company_places",'mono'))
        res.update(company_wilaya_id = int(self.env['ir.config_parameter'].sudo().get_param("sn_base.company_wilaya_id")))

        #self.wilayates=self.env['sn_base.wilayates'].search([('id', '=', 5)])
        # res.update(wilayates=self.env['sn_base.wilayates'].search([('id', '=', 5)]))
        return res


    def set_values(self):
        if self.company_places=='mono' and not self.company_wilaya_id:
            raise UserError('Vous devez choisir une wilaya, la creer s il le faut!..')
        super(SNbaseSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("sn_base.company_places",  self.company_places )
        self.env['ir.config_parameter'].sudo().set_param("sn_base.company_wilaya_id",  self.company_wilaya_id )
