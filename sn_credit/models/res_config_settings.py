from odoo import models, fields, api
class CreditsSettings(models.TransientModel):

    _inherit = 'res.config.settings'
    # TODO:: get rid of this in the future
    days_omitted_before = fields.Char(string='Nombre de jour non considéré avant declaration')

    @api.model
    def get_values(self):
        res = super(CreditsSettings, self).get_values()
        res['days_omitted_before'] = int(self.env['ir.config_parameter'].with_user(True).get_param('sn_credit.days_omitted_before', default=5))
        return res

    @api.model
    def set_values(self):
        super(CreditsSettings, self).set_values()
        self.env['ir.config_parameter'].with_user(True).set_param('sn_credit.days_omitted_before', self.days_omitted_before)

