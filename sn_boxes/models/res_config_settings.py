from odoo import api, fields, models

class ResConfigBoxesSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_client_payment = fields.Boolean(string='Afficher les paiements des clients', config_parameter='sn_boxes.show_client_payment')
    show_supplier_payment = fields.Boolean(string='Afficher les réglements des fournisseurs',  config_parameter='sn_boxes.show_supplier_payment')
