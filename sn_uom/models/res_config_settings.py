from odoo import models, fields, api


class AchatSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    show_uom = fields.Boolean(string="Afficher les unités de mesures avec les pièces de document",config_parameter='sn_uom.show_uom',default=True)
