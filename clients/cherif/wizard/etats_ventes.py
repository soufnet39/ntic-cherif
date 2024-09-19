from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime
from dateutil.relativedelta import relativedelta

class wiz_commandes(models.TransientModel):
    _name = 'cherif.commandes.wiz1'

    def _default_year(self):
        now = datetime.datetime.now()
        return str(now.year)

   
    contrat_ids = fields.Many2many(comodel_name="sn_credit.contrats", string="Contrat", required=True )

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
    lines_ids = fields.One2many('cherif.commandes.wiz1.lines', 'wiz_id' , string='Lignes de Ventes', readonly=True)
    
    date_operation = fields.Date(
        string='Date',
        default=fields.Date.context_today,
    )
    show_prices = fields.Selection(
        string='Afficher les prix',
        selection=[('yes', 'Oui'),('no', 'Non')],
        default='yes',
        required=True
        )


    @api.onchange( 'periode', 'mois', 'annee')
    def clear_lines_ids(self):
        self.lines_ids=[]

    ######################
   
    def get_commandes_lines(self):
        self.lines_ids=[]
        yr= int(self.annee)
        conditions=[('operation_type','=','command'),('state','not in',['canceled']),('contrat', 'in', self.contrat_ids.ids)]

      
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
            gr = self.env['sn_sales.commande.lines'].read_group(
                [('commande_id', 'in', commandes_ids)],  
                fields=['name','price_unit:avg' , 'qty:sum','price_total:sum'], 
                groupby=['name','price_unit']  
            )
           
            filb_values = [(0, 0, {
                               'name': group['name'],
                               'price_unit': group['price_unit'],
                               'qty': group['qty'],
                               'montant': group['price_total']                        
                               }) for group in gr]

            self.lines_ids = [(5, 0, 0)]  # to empty records first

            self.lines_ids = filb_values

    def print_etats_commandes_lines(self):
        return self.env.ref('cherif.commandes_lines_report').report_action(self)

class wiz_commandes_lines(models.TransientModel):
        _name = "cherif.commandes.wiz1.lines"

        wiz_id = fields.Many2one('cherif.commandes.wiz1', string='Etat en relation')
       
        name = fields.Char('Article' )
        price_unit = fields.Float(string="CCP" , digits="montant" )
        qty    = fields.Integer(string="Qte." )
        montant = fields.Float(string="Total", digits="montant" )
