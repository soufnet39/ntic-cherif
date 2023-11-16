from odoo import models, fields, api


class AchatSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    vaiants_exists = fields.Boolean(string="Proposer des différentes variants pour le même produit",config_parameter='sn_varants.vaiants_exists',default=False)
