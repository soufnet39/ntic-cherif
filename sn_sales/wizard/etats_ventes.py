from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime
from dateutil.relativedelta import relativedelta

class wiz_commandes(models.TransientModel):
    _name = 'sn_sales.commandes.wiz1'

    def _default_year(self):
        now = datetime.datetime.now()
        return str(now.year)

    etat = fields.Selection(
        string='Etat1',
        selection=[
            ('client', 'Par Client'), 
            ('global', 'Etat global des Clients')],
        default='client', required = True )
    client_id = fields.Many2one('sn_sales.partner', string='Client',domain=[('is_customer','=',True)])  
    client_code = fields.Char('Code Client') 

    etat_vendeur = fields.Selection(
        string='Etat2',
        selection=[
            ('all', 'Tous les Vendeurs'), 
            ('one', 'Par Vendeur')],
        default='all', required = True )
    user_id = fields.Many2one('res.users', string='Vendeur',domain=[('name','!=','Administrator')])

    periode = fields.Selection(
        string='Période',
        selection=[('mois', 'Monsuel'), ('trimestre', 'Trimestriel'),
        ('semestre', 'Semestriel'), ('annuel', 'Annuel'),('interval', 'Interval'),('global', 'Global')],
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
    
    trimestre = fields.Selection(
        string='Trimestre',
        selection=[('1', '1er Trimestre'), ('2', '2em Trimestre'),
        ('3', '3em Trimestre'), ('4', '4em Trimestre')]
        )

    semestre = fields.Selection(
        string='Semestre',
        selection=[('1', '1er Semestre'), ('2', '2em Semestre')]
        )

    annee = fields.Selection(
        string='Année',
        selection=[('2019', 2019), ('2020', 2020), ('2021', 2021),('2022', 2022),('2023', 2023),('2024', 2024)],
        default=_default_year,
        required=True
        )
    commandes_ids = fields.Many2many('sn_sales.commandes',  string='Commandes de Ventes', compute="get_commandes")
    
    date_operation = fields.Date(
        string='Date',
        default=fields.Date.context_today,
    )

    @api.onchange('client_id','user_id', 'periode', 'mois', 'trimestre', 'semestre', 'annee')
    def clear_invoices_ids(self):
        self.commandes_ids=[]

    ######################
    #OVERWITTEN IN ALBELT#
    ######################
    def get_commandes(self):
        yr= int(self.annee)
        conditions=[('operation_type','=','command'),('state','not in',['canceled'])]

        if self.etat=='client':
            if self.client_id:
                conditions.append(('partner_id', '=', self.client_id.id))
            #else:            
                #raise ValidationError('Vous devez choisir un client d abord.')
        if self.etat_vendeur=='one':
            if self.user_id.id:
                conditions.append(('user_id', '=', self.user_id.id))
        if self.periode=='mois':
            ms=int(self.mois)
            conditions.append(('confirmation_date','>=',datetime.datetime(yr, ms, 1).strftime('%Y-%m-%d')))
            conditions.append(('confirmation_date','<=',(datetime.datetime(yr, ms, 1)+relativedelta(months=+1,days=-1) ).strftime('%Y-%m-%d')))
        if self.periode=='trimestre':
            tr=int(self.trimestre)
            conditions.append(('confirmation_date','>=',datetime.datetime(yr, (tr-1)*3+1, 1)))
            conditions.append(('confirmation_date','<=',(datetime.datetime(yr, (tr-1)*3+3, 1, 1)+relativedelta(months=+1,days=-1) )))
        if self.periode=='semestre':
            sm=int(self.semestre)
            conditions.append(('confirmation_date','>=',datetime.datetime(yr, (sm-1)*6+1, 1)))
            conditions.append(('confirmation_date','<=',(datetime.datetime(yr, (sm-1)*6+6, 1, 1)+relativedelta(months=+1,days=-1) )))
        if self.periode=='annuel':
            conditions.append(('confirmation_date','>=',datetime.datetime(yr, 1, 1)))
            conditions.append(('confirmation_date','<=',datetime.datetime(yr, 12, 31)))
        if self.periode=='interval':
            if self.date_debut:
                conditions.append(('confirmation_date', '>=', self.date_debut))
            if self.date_fin:
                conditions.append(('confirmation_date', '<=', self.date_fin))
            
        self.commandes_ids = self.env['sn_sales.commandes'].search(conditions)

    def print_etats_commandes(self):
        return self.env.ref('sn_sales.action_etats_commandes_report').report_action(self)
