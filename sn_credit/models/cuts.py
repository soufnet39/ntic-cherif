from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import base64

def get_years():
    year_list = []
    for i in range(2019, 2036):
        year_list.append((str(i), str(i)))
    return year_list
def get_months():
    return [('1', 'Janvier'), ('2', 'Février'), ('3', 'Mars'), ('4', 'Avril'),
            ('5', 'Mai'), ('6', 'Juin'), ('7', 'Juillet'), ('8', 'Août'),
            ('9', 'Septembre'), ('10', 'Octobre'), ('11', 'Novembre'), ('12', 'Decembre'), ]


class NticCuts(models.Model):
    _name = "sn_credit.cuts"
    _description = 'coupure par mois'
    _order = 'id desc'

    name = fields.Char(string="Intitulé de l'enlèvement", required=True, copy=False,)  #index=True, compute='_tasmiya'
    sequence = fields.Integer(string='Sequence', default=10)
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company.id)
    #c_month = fields.Selection(get_months(), string="Mois", required=True, default=lambda x: str(datetime.today().month))
    #c_year = fields.Selection(get_years(), string="Année", required=True, default=lambda x: str(datetime.today().year))
    cuts_lines = fields.One2many('sn_credit.cuts.lines', 'cut_id', string='Une ligne de listing', copy=False )
    cuts_tempo_lot_ids = fields.One2many('sn_credit.tempo_cuts.lines', 'cut_id', string='Lots', copy=False )

    nbr_lines = fields.Integer(string="Lignes", compute='_nbr_lignes', store=True )
    nbr_cuts_tempo_lot = fields.Integer(string="Lignes", compute='_nbr_cuts_tempo_lot', store=True )

    files = fields.Binary(string="Upload Txt File", )
    filename = fields.Char()
    count_pay = fields.Integer('Compteur payés', default=0, store=True,  compute='_hisab_mta')
    count_imp = fields.Integer('Compteur Impayés', default=0, store=True,  compute='_hisab_mta')
    count_blo = fields.Integer('Compteur Bloqués', default=0, store=True,  compute='_hisab_mta')
    count_clo = fields.Integer('Compteur Clôturé', default=0, store=True,  compute='_hisab_mta')
    count_ind = fields.Integer('Compteur Indéfinis', default=0,store=True,  compute='_hisab_mta')

    mta_pay = fields.Float('Mta. payés', default=0, store=True,  compute='_hisab_mta')

    calcule_done = fields.Boolean("Calcule done",default=False,store=False )


    _sql_constraints = [
        ('month_year_unique2', 'unique(id)', #c_month,c_year,company_id,
         'Des prèlevements sont identiques , Ils doivent être uniques!'),
    ]

    @api.depends('cuts_lines')
    def _nbr_lignes(self):
        for rec in self:
            rec.nbr_lines = len(rec.cuts_lines)

    @api.depends('cuts_tempo_lot_ids')
    def _nbr_cuts_tempo_lot(self):
        for rec in self:
            rec.nbr_cuts_tempo_lot = rec.cuts_tempo_lot_ids.search_count([('cut_id','=',rec.id),('done','=',False)])

    # @api.onchange('cuts_tempo_lot_ids.done')
    # def _get_dones(self):
    #     res = {}
    #     res['domain'] = {'cuts_tempo_lot_ids': [('done', '=', False)]}
    #     return res

    # @api.depends('c_month', 'c_year')
    # def _tasmiya(self):
    #     mois_list = get_months()
    #     moi = [l[1] for l in mois_list][int(self.c_month) - 1]
    #     self.name = 'Enlèvement ' + moi + ' ' + self.c_year
    #     self.sequence = int(self.c_year) + int(self.c_month)

    @api.depends('nbr_lines')
    def _hisab_mta(self):
        for s in self:
            if not isinstance(s.id, models.NewId):
                ss = s.cuts_lines.search([('cut_id','=',s.id),('c_etat', '=', '0')])
                s.count_pay=len(ss)
                s.mta_pay=sum(ss.mapped('c_montant'))

                ss = s.cuts_lines.search([('cut_id','=',s.id),('c_etat', '=', '1')])
                s.count_imp=len(ss)

                ss = s.cuts_lines.search([('cut_id','=',s.id),('c_etat', '=', '2')])
                s.count_blo=len(ss)

                ss = s.cuts_lines.search([('cut_id','=',s.id),('c_etat', '=', '5')])
                s.count_clo=len(ss)

                ss = s.cuts_lines.search([('cut_id','=',s.id),('c_etat', '=', 'x')])
                s.count_ind=len(ss)



    @api.onchange('filename', 'files')
    def onchange_method(self):
        if self.files:
            # Check the file's extension
            tmp = self.filename.split('.')
            ext = tmp[len(tmp) - 1]
            if ext.upper() != 'TXT':
                self.update({
                    'filename': '',
                    'files': ''
                })
                raise ValidationError(_("The file must be a TXT file"))
            else:
                ####################
                portee=2000
                ####################
                ff = base64.standard_b64decode(self.files)
                lines = ff.decode().split('\n')
                tempo_new_lines = []
                compteur=0
                compteur_lot=0
                cum_lot=""

                for line in lines:

                    ref = line[74:].rstrip()
                    # must take lines that belongs to that company (ex: 31:Oran)
                    if self.env.company.code_centre==ref[-2:]:
                        if len(line.strip())>70:
                            compteur += 1
                            cum_lot += line

                            if compteur>=portee:
                                tempo_new_lines.append((0, 0, {
                                    'cut_id': self.id,
                                    'lot':cum_lot,
                                    'lot_title':str(compteur_lot*portee+1)+" - "+str((compteur_lot+1)*portee)
                                    }))
                                compteur=0
                                compteur_lot+=1
                                cum_lot=""


                if compteur>0:
                    tempo_new_lines.append((0, 0, {
                            'cut_id': self.id,
                            'lot':cum_lot,
                            'lot_title':str(compteur_lot*portee+1)+" - "+str(compteur_lot*portee+compteur)
                            }))
                self.cuts_tempo_lot_ids = tempo_new_lines




    def print_cuts(self):
        return self.env.ref('sn_credit.action_report_cuts').report_action(self)

    def recalcule_reel_month(self):
        for rec in self.cuts_lines:
            j_cut = rec.c_date.day
            j_contrat = rec.aksat_line_id.jour_prelevement
            if (j_cut<j_contrat):
                dt=(rec.c_date + relativedelta(months=-1))
                rec.mois_reel=dt.month
                rec.annee_reel=dt.year
            else:
                rec.mois_reel= rec.c_mois
                rec.annee_reel= rec.c_annee
    def control_duplicates(self):
        query='''SELECT name FROM public.sn_credit_cuts_lines where cut_id=%s and c_etat='0'  group by name,c_ccp,c_etat,mois_reel having count(*)>1'''
        self.env.cr.execute(query % (self.id))
        query_result = self.env.cr.fetchall()
        if query_result:
            halat=set(list(map(lambda x:x[0][2:6], query_result)))
            strr = "\n   - ".join(halat)
            raise UserError(_('Attension: Commande(s) avec recettes doublés:\n   - ')+strr)
        else:
            raise UserError(_('Très bien; Pas de recettes doublés '))

    def remove_duplicates(self):
        query='''SELECT max(id) as idx FROM public.sn_credit_cuts_lines where cut_id=%s and c_etat='0'  group by name,c_ccp,c_etat,mois_reel having count(*)>1'''
        self.env.cr.execute(query % (self.id))
        query_result = self.env.cr.fetchall()
        if query_result:
            halat=list(map(lambda x:x[0], query_result))
            strr = ",".join([ str(i) for i in halat])
            query='''delete from public.sn_credit_cuts_lines where  id in (%s)'''
            self.env.cr.execute(query % (strr))
            self.env.cr.commit()
            raise UserError(_('Suppression términé avec succée.'))
            
        else:
            raise UserError(_('Pas de cas doublé'))
    def calculator(self):
        query='''
        update  public.sn_sales_commandes set payment_state='waloo',amount_rest=amount_ttc where not coalesce(is_considered_as_retard, false) ;
        update  public.sn_sales_commandes set 
            total_deduit= qr.tot_ded, 
            amount_rest=amount_ttc - qr.tot_ded - total_reglement,
            payment_state = CASE
                        WHEN qr.tot_ded=0 THEN 'waloo'
                        WHEN amount_ttc - qr.tot_ded=0 THEN 'complet'
                        WHEN (amount_ttc - qr.tot_ded)>0 and qr.tot_ded>0 THEN 'partiel'
                        WHEN (amount_ttc - qr.tot_ded)<0 THEN 'negatif'
                    END
        from 
        (SELECT aksat_id,sum(mta_deduit) as tot_ded FROM public.sn_credit_aksats_mois_reel  group by aksat_id ) as qr
        where id=qr.aksat_id and not coalesce(is_considered_as_retard, false);
        '''
        self.env.cr.execute(query)
        self.calcule_done=True



        


class NticCutsLines(models.Model):
    _name = "sn_credit.cuts.lines"
    _description = "detail mensuel des cuts faites par la poste"
    _order = 'cut_id,  id'

    name = fields.Char(string="Réference",)

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)

    aksat_line_id = fields.Many2one('sn_credit.aksats.lines', string="link 2 aksats",)

    commande_aksat_line_id = fields.Integer(string="", related='aksat_line_id.aksat_id.id', store=True )

    cut_id = fields.Many2one('sn_credit.cuts', string='Réference2Cut',
                               required=True, ondelete='cascade',
                               index=True, copy=False, readonly=True)

    c_ccp = fields.Char(string="CCP Client",  )
    c_nom = fields.Char(string="Nom",  )
    c_montant = fields.Float(string="Montant")
    c_date = fields.Date(string="Date",)
    c_mois =  fields.Integer(string="Mois")
    c_annee =  fields.Integer(string="Année")
    mois_reel =  fields.Integer(string="Mois réel",compute="extract_reel_month",store=True)
    annee_reel =  fields.Integer(string="Année réel",compute="extract_reel_month",store=True)
    p_ccp = fields.Char(string="CCP Vendeur",  )
    c_etat = fields.Selection(string="Etat", selection=[
        ('0', 'Payé'),
        ('1', 'Impayé'),
        ('2', 'Bloqué'),
        ('5', 'Clôturé'),
        ('x', 'Indéfini'),
        ('y', 'Sans Image'),
    ], required=False, default='x')


    @api.depends('c_date')
    def extract_reel_month(self):
        for rec in self:
            j_cut = rec.c_date.day
            j_contrat = rec.aksat_line_id.jour_prelevement
            if (j_cut<j_contrat):
                dt=(rec.c_date + relativedelta(months=-1))
                rec.mois_reel=dt.month
                rec.annee_reel=dt.year
            else:
                rec.mois_reel= rec.c_mois
                rec.annee_reel= rec.c_annee
   


class NticTempoCutsLines(models.Model):
    _name = "sn_credit.tempo_cuts.lines"
    _description = "Cuts text file divided par lots"

    cut_id = fields.Many2one('sn_credit.cuts', string='Réference2Cut',
                               required=True, ondelete='cascade',
                                copy=False, readonly=True)

    lot = fields.Text( string='lot')
    lot_title = fields.Text( string='Intervale')
    done = fields.Boolean("Done" , default=False)


    def convert_lot(self):
        selected_lot = self.env.context["selected_lot"]
        lines = selected_lot.split('\r')
        new_lines = []
        aksats_lines = self.env['sn_credit.aksats.lines']
        for line in lines:

            #012345678901234567890123456789012345678901234567890123456789012345678901234567890
            #0001405133MLLE MEDIAIRE MIMOUNA      00000003100.0023/08/2017002100326000054/2017
            #c_ccp.....c_nom......................c_montant.....c_date....p_ccp.....e..name

            aksat_line_id = False

            if len(line.strip())>70:
                eta = line[71:72]
                eta = eta if (eta == '0' or eta == '1' or eta == '2' or eta == '5') else 'x'
                ref = line[74:].rstrip()
                # must take lines that belongs to that company (ex: 31:Oran)
                if self.env.company.code_centre==ref[-2:]:
                    liens=aksats_lines.search([('name','=',ref)]).ids
                    if (liens):
                        aksat_line_id=liens[0]
                        didi = datetime.strptime(line[51:61], '%d/%m/%Y').date()
                        mta = float(line[37:51])
                        new_lines.append((0,0, {
                            'name': ref,
                            'cut_id': self.cut_id.id,
                            'aksat_line_id':aksat_line_id,
                            'c_ccp': line[0:10],
                            'c_nom': line[10:37],
                            'c_montant': mta,
                            'c_date': didi,
                            'c_mois': didi.month,
                            'c_annee': didi.year,
                            'p_ccp': line[61:71],
                            'c_etat': eta,
                            #line[42:45] 2Chars not concerned
                        }))
                    else:
                        eta = 'y'
                        aksat_line_id = 0

        if len(new_lines)>0:
            self.cut_id.write({'cuts_lines':new_lines})
            self.done=True
