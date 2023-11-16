from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
from dateutil.relativedelta import relativedelta
from odoo.osv import osv
class wiz_system_errors(models.TransientModel):
    _name = 'sn_credit.system_errors'

    name = fields.Char('Name', default='default')
    prelevement_ids = fields.Many2many('sn_credit.prelevements', string='Prélèvements')

    commandes_ids = fields.Many2many(
        string='commandes',
        comodel_name='sn_sales.commandes',
        relation='system_errors_commandes',
        column1='name',
    )

    decalage = fields.Selection(string='Décalage', selection=[('1', '1 mois'), ('2', '2 mois'), ('3', '3 mois')], default='1', required=True)

    mode = fields.Selection(
        string='Mode de traitement',
        selection=[('all', 'Traiter la totalité'), ('selection', 'valor2')]
    )

    hala = fields.Selection(string='Hala', selection=[
        ('waiting', 'waiting'),
        ('clear', 'clear'),
        ('exist', 'exist'),
        ('done', 'Done')
        ]
        , default='waiting' )


    def do_it(self):
        prelevements = self.prelevement_ids
        list_refs = []
        if len(prelevements) == 0:
            raise UserError(_('Pas de prélèvement choisis'))
        ids= self.prelevement_ids.mapped('id')

        query="""
        select db1.aksat_id, COALESCE(db2.cnt,0) as adad from (
            SELECT aksat_id FROM public.sn_credit_aksats_lines 
            where  prelevement_id in %s
            group by aksat_id
            ) db1 left join
            (SELECT commande_aksat_line_id as cali , count(id) as cnt
            FROM public.sn_credit_cuts_lines 
            where company_id=%s
            group by cali
            ) db2
            on db1.aksat_id = db2.cali
            where COALESCE(db2.cnt,0)=0
            """
        # query="""
        #   SELECT al.prelevement_id,al.aksat_id,al.id,count(cl.id) as clcount  FROM public.sn_credit_aksats_lines al 
        #     left join public.sn_credit_cuts_lines cl 
        #     on al.id = cl.aksat_line_id
        #     where al.prelevement_id in %s
        #     group by al.prelevement_id,al.aksat_id,al.id
        #     having count(cl.id)=0
        #     """
        
        self.env.cr.execute(query,(tuple(ids),self.env.company.id))
        query_result = self.env.cr.dictfetchall()

        if len(query_result) == 0:
            self.hala = 'clear'
        else:
            list_refs = map(lambda x: x['aksat_id'], query_result)
            list_refs = sorted(list(set(list_refs)))
            self.hala = 'exist'
            self.commandes_ids=list_refs

    def trait_all(self):
        #commandes = self.commandes_ids
        for rec in self.commandes_ids:
            rec.date_start = rec.date_start + relativedelta(months=int(self.decalage))
        idz= self.commandes_ids.ids
        aksats= self.env['sn_credit.aksats.lines'].search([('aksat_id','in',idz)]) 
        for rec in aksats:
            rec.day_to_cut = rec.day_to_cut + relativedelta(months=int(self.decalage))
            rec.moi = rec.day_to_cut.month
            rec.annee = rec.day_to_cut.year
            rec.prelevement_id= False
        self.hala = 'done'    
        
      