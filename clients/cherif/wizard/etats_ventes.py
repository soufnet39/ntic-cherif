from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime
from dateutil.relativedelta import relativedelta

class wiz_commandes(models.TransientModel):
    _name = 'cherif.commandes.wiz1'

    def _default_year(self):
        now = datetime.datetime.now()
        return str(now.year)

   
    
    periode = fields.Selection(
        string='Période',
        selection=[('mois', 'Mensuel'), ('annuel', 'Annuel'),('interval', 'Interval'),('global', 'Global')],
        default='mois', required = True )
    
    date_debut = fields.Date(
        string='Date Début',
        default=fields.Date.context_today,
    )
    date_fin = fields.Date(
        string='Date Fin',
        default=fields.Date.context_today,
    )
    

    mois = fields.Selection(
        string='Mois',
        selection=[
            ('1', 'Janvier'),
            ('2', 'Février'),
            ('3', 'Mars'),
            ('4', 'Avril'),
            ('5', 'Mai'),
            ('6', 'Juin'),
            ('7', 'Juillet'),
            ('8', 'Août'),
            ('9', 'Septembre'),
            ('10', 'Octobre'),
            ('11', 'Novembre'),
            ('12', 'Décembre')]
        )
    

    annee = fields.Selection(
        string='Année',
        selection=[('2023', 2023),('2024', 2024),('2025', 2025),('2026', 2026)],
        default=_default_year,
        required=True
        )
    commandes_lines_ids = fields.Many2many('sn_sales.commande.lines',  string='Lignes de Commandes de Ventes', compute="get_commandes_lines")
    
    date_operation = fields.Date(
        string='Date',
        default=fields.Date.context_today,
    )

    @api.onchange( 'periode', 'mois', 'annee')
    def clear_commandes_lines_ids(self):
        self.commandes_lines_ids=[]

    ######################
   
    def get_commandes_lines(self):
        yr= int(self.annee)
        conditions=[('operation_type','=','command'),('state','not in',['canceled'])]

      
        if self.periode=='mois':
            ms=int(self.mois)
            conditions.append(('confirmation_date','>=',datetime.datetime(yr, ms, 1).strftime('%Y-%m-%d')))
            conditions.append(('confirmation_date','<=',(datetime.datetime(yr, ms, 1)+relativedelta(months=+1,days=-1) ).strftime('%Y-%m-%d')))
        if self.periode=='annuel':
            conditions.append(('confirmation_date','>=',datetime.datetime(yr, 1, 1)))
            conditions.append(('confirmation_date','<=',datetime.datetime(yr, 12, 31)))
        if self.periode=='interval':
            if self.date_debut:
                conditions.append(('confirmation_date', '>=', self.date_debut))
            if self.date_fin:
                conditions.append(('confirmation_date', '<=', self.date_fin))
            
        commandes_ids = self.env['sn_sales.commandes'].search(conditions).ids
        if commandes_ids:
            self.commandes_lines_ids = self.env['sn_sales.commande.lines'].search([('commande_id','in',commandes_ids)])


    def print_etats_commandes_lines(self):
        return self.env.ref('cherif.commandes_lines_report').report_action(self)
