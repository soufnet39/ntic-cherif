from odoo import api, fields, models


class ResFactureConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    facture_note_default = fields.Char(string='Note à afficher après chaque facture', config_parameter='sn_invoices.facture_note_default')
    facture_confirmed_by_default = fields.Boolean("Factures confirmées par défaut", config_parameter='sn_invoices.facture_confirmed_by_default')
