# -*- coding: utf-8 -*-
# Copyright (c) 2016  - Osis


from odoo import api, fields, models,_
from odoo.exceptions import UserError

class SnSalesTimbre(models.Model):
    _inherit = ['mail.thread']
    _name='sn_sales.timbres'
    _description='Fiscal Timbre configuration'

    name =  fields.Char('Nom', required=True)
    taux = fields.Float('Taux du timbre',  required=True)
    max_value = fields.Float('Plafond',  required=True)
    date_application_start = fields.Date(string="Applicable à partir de", required=True, )
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Le nom doit être unique par Société!'),
    ]

    @api.model
    def _timbre(self, montant,date_facture):
        res = 0.0
        timbre_obj = self.env['sn_sales.timbres']
        liste_obj  = timbre_obj.search([])
        if not liste_obj :
           raise UserError(_('Pas de confiuration du calcul Timbre.'))

        #compare between date_facture and date_application_start
        dicta = liste_obj[-1]

        res = montant * dicta['taux']
        res = min(dicta['max_value'],res)
      

        #res['amount_timbre'] = montant + calcule_timbre
        return res