from odoo import models, fields, api, _
#from odoo.exceptions import UserError, ValidationError

class NticWilayates2Centres(models.Model):
    _inherit = 'sn_base.wilayates'

    @api.model
    def create(self, vals):
        cmpny= self.env['res.company']
        cmpny.create({
           'code_centre': vals['code'],
            'name': vals['name']
        })


        record = super(NticWilayates2Centres, self).create(vals)
        return record

    def write(self, vals):
        cmpny = self.env['res.company'].search([('code_centre','=', self.code)])
        cmpny.update({
            'code_centre': self.code,
            'name': self.name
        })
        super(NticWilayates2Centres, self).write(vals)
        return True


