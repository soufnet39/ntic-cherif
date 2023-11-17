from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from odoo.tools import date_utils


def get_years():
    year_list = []
    for i in range(2019, 2036):
        year_list.append((str(i), str(i)))
    return year_list
def get_months():
    return [('1', 'Janvier'), ('2', 'Février'), ('3', 'Mars'), ('4', 'Avril'),
            ('5', 'Mai'), ('6', 'Juin'), ('7', 'Juillet'), ('8', 'Août'),
            ('9', 'Septembre'), ('10', 'Octobre'), ('11', 'Novembre'), ('12', 'Decembre'), ]
def get_hokool():
    return [['client_ccp_numero', 'CompteA', 'C'],
                    ['client_ccp_cle', 'Cle', 'C'],
                    ['client_nom', 'NOM', 'C'],                   
                    ['amount', 'MontantVo', 'F'],
                    ['contrat_ccp_numero', 'CompteB', 'C'],
                    ['contrat_ccp_cle', 'Cle1', 'C'],
                    ['date_start', 'DateDebut', 'D'],
                    ['date_end', 'DateFin', 'D'],
                    ['date_start', 'DateCreation', 'D'],
                    ['mth_traited', 'MoisTraite', 'I'],
                    ['nbr_echeance', 'Nbrecheance', 'I'],
                    ['jour_prelevement', 'JourPrel', 'I'],
                    ['name', 'Reference', 'C'],
                    ]

class NticPrelevements(models.Model):
    _name = "sn_credit.prelevements"
    _description = "Prélèvements de aksats par mois"
    _order = 'id desc'

    name = fields.Char(string='Mois et Année', readonly=True, copy=False, index=True, default='/', )
    sequence = fields.Integer(string='Sequence', default=10)
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company.id)

    c_month = fields.Selection(get_months(),string="Mois", required=True, default= lambda x:  str(datetime.today().month))
    c_year = fields.Selection(get_years(), string="Année", required=True, default= lambda x:  str(datetime.today().year))

    aksats_lines = fields.One2many('sn_credit.aksats.lines', 'prelevement_id', string='Une ligne prelevée', copy=False, )
    nbr_lines = fields.Integer(string="Nbr lignes", compute='_nbr_lignes', )
    nbr_lines_a = fields.Integer(string="Nbr lignes Contrat A", compute='_nbr_lignes', )
    nbr_lines_b = fields.Integer(string="Nbr lignes Contrat B", compute='_nbr_lignes', )
    nbr_lines_c = fields.Integer(string="Nbr lignes Contrat C", compute='_nbr_lignes', )
    nbr_lines_d = fields.Integer(string="Nbr lignes Contrat D", compute='_nbr_lignes', )
    nbr_lines_e = fields.Integer(string="Nbr lignes Contrat E", compute='_nbr_lignes', )
    nbr_lines_f = fields.Integer(string="Nbr lignes Contrat F", compute='_nbr_lignes', )
    a_exist= fields.Boolean(string="A exist", default=False  )
    b_exist= fields.Boolean(string="B exist", default=False  )
    c_exist= fields.Boolean(string="C exist", default=False  )
    d_exist= fields.Boolean(string="D exist", default=False  )
    e_exist= fields.Boolean(string="E exist", default=False  )
    f_exist= fields.Boolean(string="F exist", default=False  )

    is_closed = fields.Boolean(string="Is Closed", default=False  )
    closed_on_nfact = fields.Char("Numéro de facture" , )
    closed_on_idfact = fields.Integer("Numéro de facture" , )
    
    _sql_constraints = [
        ('month_year_unique', 'unique(c_month,c_year,company_id)', 'Le mois et l\'année sont déjà prises, Ils doivent être uniques!'),
    ]


    @api.depends('aksats_lines')
    def _nbr_lignes(self):
        self.nbr_lines = len(self.aksats_lines)
        self.nbr_lines_a = len(self.aksats_lines.filtered(lambda r: r.contrat=="A"))
        self.nbr_lines_b = len(self.aksats_lines.filtered(lambda r: r.contrat=="B"))
        self.nbr_lines_c = len(self.aksats_lines.filtered(lambda r: r.contrat=="C"))
        # self.nbr_lines_d = len(self.aksats_lines.filtered(lambda r: r.contrat=="D"))
        # self.nbr_lines_e = len(self.aksats_lines.filtered(lambda r: r.contrat=="E"))
        # self.nbr_lines_f = len(self.aksats_lines.filtered(lambda r: r.contrat=="F"))

    def print_prelevements(self):
        return self.env.ref('sn_credit.action_report_prelevements').report_action(self)

    def print_prelevements_xlsx(self):
        if (not self.is_closed):
            self.call_aksats()
        report = self.env.ref('sn_credit.prelevements_xlsx')
        report.report_file = self.name
        return report.report_action(self, data={'any': False,'moi':self.c_month,'annee':self.c_year})


    def call_aksats(self):
        #  self.env['sn_sales.commandes'].search([('moi', '=', int(self.c_month)) ])
        if self.is_closed:
             raise UserError(_("Prelevement férmé! Il faut l'a re-ouvert pour importer de nouveau."))

        cases_not_traited = self.env['sn_sales.commandes'].search([
                                        ('date_start', '>=',date_utils.start_of(fields.Date.today(), 'month')),
                                        ('aksats_adad', '=', 0),
                                        ('state', '=', 'confirmed'),
                                        ('operation_type', '=', 'command'),
                                        ] )
        if len(cases_not_traited) > 0:
            strr = "\n   - ".join(map(lambda x: x['name'],cases_not_traited))
            raise UserError(_('Attension: Commande(s) non traité(s):\n   - ')+strr)
        
        query='''select cmds.name from(SELECT DISTINCT aksat_id FROM public.sn_credit_aksats_lines where prelevement_id=%d group by name,aksat_id  having count(id)>1 order by aksat_id) as halat left join public.sn_sales_commandes as cmds on halat.aksat_id=cmds.id'''
        self.env.cr.execute(query % (self.id))
        query_result = self.env.cr.fetchall()
        if len(query_result)>0:
           strr = "\n   - ".join(list(map(lambda x: x[0],query_result)))
           raise UserError(_('Attension: Aksats Doublés pour le commandes:\n   - ')+strr)
  


        #------------------------------

        # query="""
        #   SELECT al.prelevement_id,al.aksat_id,al.id,count(cl.id) as clcount  FROM public.sn_credit_aksats_lines al 
        #     left join public.sn_credit_cuts_lines cl 
        #     on al.id = cl.aksat_line_id
        #     where al.prelevement_id in %s
        #     group by al.prelevement_id,al.aksat_id,al.id
        #     having count(cl.id)=0
        #     """
        
        # self.env.cr.execute(query,(tuple(ids),self.env.company.id))
        # query_result = self.env.cr.dictfetchall()
        #------------------------------

        aksats= self.env['sn_credit.aksats.lines'].search([('moi', '=', int(self.c_month)),
                                                           ('annee', '=', int(self.c_year)),
                                                           ('state_parent', '=', 'confirmed'),
                                                           ])
        contrats=list(dict.fromkeys(aksats.mapped('contrat')))
        self.a_exist = 'A' in contrats
        self.b_exist = 'B' in contrats
        self.c_exist = 'C' in contrats
        self.d_exist = 'D' in contrats
        self.e_exist = 'E' in contrats
        self.f_exist = 'F' in contrats
        if len(aksats)==0:
            raise UserError(_('Désolé.. Pas de prélèvement pour ce mois!..'))
        else:
            aksats.update({'prelevement_id': self.id})
        return True
    def lock_it(self):
        #last_one=self.aksats_lines.search([('prelevement_id','=',self.id)],limit=1,order="id DESC")
        qr='''SELECT name,aksat_id FROM public.sn_credit_aksats_lines  where prelevement_id=%s group by name,aksat_id having count(*)>1'''
        self.env.cr.execute(qr % (self.id))
        query_result = self.env.cr.fetchall()
        if query_result:
            halat=set(list(map(lambda x:x[0][2:6], query_result)))
            strr = "\n   - ".join(halat)
            raise UserError(_('Attension: Commande(s) avec AKSAT doublés:\n   - ')+strr)



        list_cmd_ids=self.aksats_lines.search([('prelevement_id','=',self.id)]).mapped('aksat_id').mapped('id')

        list_cmd_ids.sort()
        if(list_cmd_ids):             
            self.is_closed = True 
            self.closed_on_idfact = list_cmd_ids[-1]  
            last_hala=self.env['sn_sales.commandes'].search([('id', '=', list_cmd_ids[-1])])
            if last_hala:
               self.closed_on_nfact = last_hala.name  
   
    def unlock_it(self):
        self.is_closed = False 
        self.closed_on_nfact = "" 
        self.closed_on_idfact = 0  


    @api.model
    def create(self, vals):
         mois_list = get_months()
         moi = [l[1] for l in mois_list][int(vals['c_month'])-1]

         record = super(NticPrelevements, self).create(vals)
         record.update({'name': 'Prélèvement '+moi+' '+vals['c_year'],
                        'sequence': int(vals['c_year'])+int(vals['c_month'])})
         return record


class PrelevementsXlsx(models.AbstractModel):
        _name = 'report.sn_credit.prelevements'
        _inherit = 'report.report_xlsx.abstract'
        _description = ''

        def generate_xlsx_report(self, workbook, data, prelevements):
            hokool=get_hokool()
           
            for obj in prelevements:
                report_name = obj.name
                sheet = workbook.add_worksheet(report_name)
                bold = workbook.add_format({'bold': True})
                f_format = workbook.add_format()
                f_format.set_num_format('#,##0.00')

                d_format = workbook.add_format({'num_format': 'YYYY-mm-dd'})
                i = 0
                for h in hokool:
                    sheet.write(0, i, h[1], bold)
                    i += 1
                j=1
                for tit in obj.aksats_lines.ids:

                    t=self.env['sn_credit.aksats.lines'].browse(tit)
                    if (self.env.context["cntrt"]==t.contrat):
                        i=0
                        for h in hokool:
                            if h[2] == 'C':
                                kima=t[h[0]] or ''
                                sheet.write_string(j, i, kima)
                            elif h[2] == 'F':
                                kima = t[h[0]] or 0.0
                                sheet.write_number(j, i, kima, f_format)
                            elif  h[2]=='I':
                                kima = t[h[0]] or 0
                                sheet.write_number(j, i, kima)
                            elif h[2]=='D':
                                sheet.write_datetime(j, i, t[h[0]], d_format)

                            i+=1
                        j+=1
