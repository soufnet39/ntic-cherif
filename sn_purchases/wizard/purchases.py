from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class wiz_purchases(models.TransientModel):
    _name = 'sn_purchases.purchases.wiz1'

    def _default_year(self):
        now = datetime.datetime.now()
        return str(now.year)

    etat = fields.Selection(
        string='Etat',
        selection=[
             ('supplier', 'Par Fournisseur'), 
             ('recup', 'Etat de récupération TVA')
            ],
            default='supplier', required = True )
    supplier_id = fields.Many2one('sn_sales.partner', string='Fournisseur',domain=[('is_supplier','=',True)])  
    supplier_code = fields.Char('Code Fournisseur') 

    periode = fields.Selection(
        string='Période',
        selection=[('mois', 'Monsuel'), ('trimestre', 'Trimestriel'),
        ('semestre', 'Semestriel'), ('annuel', 'Annuel'),('global', 'Global')],
        default='mois', required = True )

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
        selection=[('2019', 2019), ('2020', 2020), ('2021', 2021), ('2022', 2022), ('2023', 2023), ('2024', 2024)], 
        default=_default_year,
        required=True
        )
    purchases_ids = fields.Many2many('sn_sales.commandes',  string='Factures Achats', compute="get_factures")
    
    date_operation = fields.Date(
        string='Date',
        default=fields.Date.context_today,
    )

    @api.onchange('supplier_id', 'periode', 'mois', 'trimestre', 'semestre', 'annee')
    def clear_invoices_ids(self):
        self.purchases_ids=[]

    
    def get_factures(self):
        yr= int(self.annee)
        conditions=[('operation_type','=','purchase')]

        if self.etat=='supplier':
            if self.supplier_id:
                conditions.append(('partner_id', '=', self.supplier_id.id))
            #else:            
                #raise ValidationError('Vous devez choisir un client d abord.')

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
        #if self.periode=='global':
            
           
        self.purchases_ids = self.env['sn_sales.commandes'].search(conditions)

    def print_etats_factures(self):
        return self.env.ref('sn_purchases.action_etats_achats_report').report_action(self)
