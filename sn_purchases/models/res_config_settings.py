from odoo import models, fields, api


class AchatSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    charges_exist = fields.Boolean(string="Activer des charges sur des produits",config_parameter='sn_purchases.charges_exist')
    purchase_confirmed_by_default = fields.Boolean("Achats confirmées par défaut",config_parameter='sn_purchases.purchase_confirmed_by_default')

