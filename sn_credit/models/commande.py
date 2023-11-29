from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class NticCreditsCommande(models.Model):
    _inherit = "sn_sales.commandes"

    # recno pour nomenclature des retraits
    recno = fields.Char(string='Recno', default='')
    cosh  = fields.Boolean(store=False)

    contrat = fields.Many2one(comodel_name="sn_credit.contrats", string="Contrat")

    code_centre = fields.Char(related='company_id.code_centre')
    #jour_retrait = fields.Integer(string="Nombre de jour", store=True)

    confirmation_date = fields.Date(string='Date', index=True, default=lambda self:fields.Date.today())

    # TODO:: add min and max for month_number field
    month_number = fields.Integer(string="Nombre des mois",  default=12)
    jour = fields.Integer('Jour', related='contrat.jour_retrait')
    date_start = fields.Date(string="Date début", default=lambda self:fields.Date.today())
    # compute on change date_start or month_number
    date_end = fields.Date(string="Date fin", readonly=True, compute='_compute_date_end',store=True)
    monthly_amount = fields.Float(string="Retrait mensuel", compute='_compute_monthly_amount', store=True )

    retrait_number = fields.Integer(string="Nbr retraits / mois",  default=4, )
    retrait_amount = fields.Float(string="Montant / Retrait",  store=True, compute='_compute_retraits')
    total_deduit = fields.Float(string="Total déduit",readonly=True) # compute='_compute_total_reglement',readonly=True

    #numero_updatable = fields.Boolean(string="Numéro éditable", defaul=False)

    payment_state = fields.Selection([
        ('waloo', 'Paiement ZERO'),
        ('partiel', 'Paiement Partiel'),
        ('complet', 'Paiement Total'),
        ('negatif', 'Paiement Négatif')
    ],
        string='Paiements', store=True, copy=False, default='waloo')

    aksats_lines = fields.One2many('sn_credit.aksats.lines', 'aksat_id', string='Une ligne de credit', copy=False, )
    aksats_mois_reel = fields.One2many('sn_credit.aksats.mois_reel_sah', 'aksat_id', string='Un mois reel de credit',) #,order='annee,moi desc' 
    
    def link_aksats_mois_reel(self):
            rid=0
            if isinstance(self.id, models.NewId): 
                rid=self._origin.id
            else:
                rid=self.id  
            if (rid):
                if self.aksats_mois_reel:
                    #Delete current linked records
                    for record in self.aksats_mois_reel:
                        self.write({'aksats_mois_reel': [(2,record.id)]})

                qr="SELECT mois_annee,mta_deduit FROM public.sn_credit_aksats_mois_reel where aksat_id=%s"
                self.env.cr.execute(qr % (rid))
                query_result = self.env.cr.fetchall()
                tot=0
                if len(query_result)>0:
                    newLines=[]
                    for r in query_result:
                        tot = tot+r[1]
                        newLines.append((0, 0, {
                            'mois_annee': r[0],
                            'mta_deduit': r[1],
                            'aksat_id': rid,                           
                        })) 
                    self.update({
                        'aksats_mois_reel': newLines,
                        'total_deduit': tot,

                        })
                    return True
                
                    
                

    aksats_adad = fields.Integer('lines number', store=True, compute='_compute_aksats_adad')
    aksats_touched = fields.Boolean('Can delete akstats')

    #### Source RETARD #####################################
    is_considered_as_retard = fields.Boolean( string='[Source] is Cmd consideré comme retard',default=False )
    retard_destination_id = fields.Integer("Cmd id image genéré comme retard")
    retard_destination_name = fields.Char("Cmd name image genéré comme retard")
    #### Target RETARD #####################################
    is_generated_from_retard = fields.Boolean("[Target] is Généré comme retard", default = False)
    retard_source_id = fields.Integer("Cmd id image consideré comme retard")
    retard_source_name = fields.Char("Cmd name image consideré comme retard")

    @api.onchange('user_id')
    def filtra_contrats(self):
        res = {}
        idds=[]
        self.contrat=0
        for r in self.env["sn_credit.contrats"].search([]):
            if self.env.user.id in r.users_ids.ids:
                idds.append(r.id)
        # stopped because the onchange method has no response, but it have to
        # if len(idds)==1:
        #     self.contrat=idds[0]
        res['domain'] = {'contrat': [('id', 'in', idds)]}
        return res

   
    # Overwrite the same function in sn_boxes.command
    @api.depends('amount_ttc') #,'payment_ids',,'aksats_mois_reel'
    def _compute_total_reglement(self):
        super(NticCreditsCommande, self)._compute_total_reglement()
        for rec in self:   
            rid=0
            if isinstance(rec.id, models.NewId): 
                rid=rec._origin.id
            else:
                rid=rec.id    
            if(rid):   
                qr="SELECT id,mta_deduit FROM public.sn_credit_aksats_mois_reel where aksat_id=%s"
                self.env.cr.execute(qr % (rid))
                query_result = self.env.cr.fetchall()
                tot = 0.0
                if query_result:
                    for r in query_result:
                        tot += r[1]
                rest = rec.amount_rest - tot  # - rec.mta_transferred_as_retard
                stt = 'waloo' if tot == 0 else ''
                stt = 'complet' if rest == 0 else ''
                stt = 'partiel' if rest > 0 and tot > 0  else ''
                stt = 'negatif' if rest < 0 else ''
                rec.update({
                    'total_deduit': tot,
                    'payment_state': stt ,
                    'amount_rest': rest,
                })

    @api.onchange('contrat')
    def reaffect_nbr_months(self):
        # the bellow line does not work with cherif ideas 
        #self.month_number = self.contrat.nbr_months
        self.retrait_number = self.contrat.nbr_aksats

    @api.onchange('contrat','confirmation_date')
    def recompute_dates(self):
        if self.jour>0 and self.jour<=31:
            dc = self.confirmation_date
            le_moi=str(dc.month)
            lannee=str(dc.year)
            prlv=self.env['sn_credit.prelevements'].search([('c_month','=',le_moi),('c_year','=',lannee)])
            closed = False
            if prlv:
               closed=prlv.mapped('is_closed')[0]

            if closed or dc >= dc.replace(day=self.jour):
                self.date_start = (dc + relativedelta(months=+1)).replace(day=self.jour)
            else:
                self.date_start=dc.replace(day=self.jour)

    @api.depends('date_start', 'month_number')
    def _compute_date_end(self):
        for rec in self:
            if rec.date_start and rec.month_number>1:
                rec.date_end = rec.date_start + relativedelta(months=+rec.month_number-1)
            else:
                rec.date_end = rec.date_start

    @api.depends('amount_ttc_sec', 'month_number')
    def _compute_monthly_amount(self):
        for rec in self:
            if rec.month_number > 0:
                rec.monthly_amount = rec.amount_ttc_sec / rec.month_number
            else:
                rec.monthly_amount = 0
        return True

    @api.depends('retrait_number', 'monthly_amount')
    def _compute_retraits(self):
        for rec in self:
            if rec.retrait_number > 0:
                rec.retrait_amount = rec.monthly_amount / rec.retrait_number
            else:
                rec.retrait_amount = 0
        return True

    @api.depends('aksats_lines') #,'aksats_lines.cuts_ids'
    def _compute_aksats_adad(self):
        for rec in self:
            rec.aksats_adad = len(rec.aksats_lines)
            # date_opera=""
            # months = []
            # aksats_av_ec_count = 0  # if always 0 => make aksats deletable

            # for al in rec.aksats_lines:
            #     aksats_av_ec_count += al.avancement + al.echecs
            #     for x in al.cuts_ids:
            #         if x.c_etat == '0':
            #             date_opera = x.c_date.strftime("%d-%b-%Y")
            #             months.append([date_opera, x.c_montant])

            # rec.aksats_touched = (aksats_av_ec_count>0)

            # values = set(map(lambda x:x[0], months))

            # newlist = [[x,sum([y[1] for y in months if y[0]==x])] for x in values]

            # mths = []
            # for el in newlist:
            #     mths.append((1, rec.id, {
            #         'date_operation': el[0],
            #         'mta_deduit': el[1],
            #     }))
            # # if len(rec.aksats_months)>0:
            # #     rec.aksats_months = [(5)]
            # rec.aksats_months = mths

    def delete_aksats(self):
        query='''SELECT max(closed_on_idfact) as mmm FROM public.sn_credit_prelevements  where is_closed=true'''
        self.env.cr.execute(query)
        query_result = self.env.cr.fetchone()
        if (query_result and self.id<(query_result[0] or 0)):
            raise UserError(_('Vous ne pouvez pas suprimer les Aksats, il appartient à un prelevement FERME'))
        else:
            for record in self.aksats_lines:
                self.write({'aksats_lines': [(2,record.id)]})
                self.special=False

    def action_generate(self):
        if round(self.retrait_number*self.retrait_amount,2) > round(self.monthly_amount,2):
           raise UserError(_('La somme des Aksats dépasse la totalité du montant par mois'))
        gasef= (round(self.retrait_number*self.retrait_amount,2) < round(self.monthly_amount,2))
        new_lines = []
        day2cut = self.date_start

        for x in range(self.retrait_number):
            new_lines.append((0, 0, {
                'name': self.contrat.name+'/'+self.recno+'/'+str(x+1).zfill(3)+'/'+self.code_centre,
                'amount': self.retrait_amount,
                'aksat_id': self.id,
                'sequence': x+1,
                'day_to_cut': day2cut,
                'moi': day2cut.month,
                'annee': day2cut.year,
                'state': 'generated',
            }))

        if gasef:
            new_lines.append((0, 0, {
                'name': self.contrat.name + '/'+self.recno+'/' + str(self.retrait_number + 1).zfill(3)+'/'+self.code_centre,
                'amount': self.monthly_amount-(self.retrait_number*self.retrait_amount),
                'aksat_id': self.id,
                'sequence': self.retrait_number+1,
                'day_to_cut':  day2cut,
                'moi': day2cut.month,
                'annee': day2cut.year,
                'state': 'generated',
            }))

        self.update({'aksats_lines': new_lines})
        return True

    def print_aksats(self):
        return self.env.ref('sn_credit.action_report_aksats').report_action(self)
    def print_avancements(self):
        return self.env.ref('sn_credit.action_report_aksats_mois').report_action(self)

    @api.model
    def create(self, vals):
        record = super(NticCreditsCommande, self).create(vals)
        record.update({'recno': record.name[3:]})
        if record.is_generated_from_retard:
           qr= "update public.sn_sales_commandes set is_considered_as_retard=True, retard_destination_name='%s' ,retard_destination_id=%s where id=%s"
           r=self.env.cr.execute(qr % (record.name,record.id,record.retard_source_id))
        return record

    def print_engagement(self):        
        return self.env.ref('sn_credit.action_report_engagement').report_action(self)
        

                                   