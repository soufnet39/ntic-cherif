from odoo import models, fields, tools, api, _
from odoo.exceptions import UserError, ValidationError


class NticAksatsLines(models.Model):
    _name = "sn_credit.aksats.lines"
    _description = "detail mensuel des retrait des aksats"
    _order = 'name'

    name = fields.Char(string="Réference", required=True,)
    aksat_id = fields.Many2one('sn_sales.commandes', string='Aksat Reference',
                               required=True, ondelete='cascade',
                               index=True,copy=False)
    prelevement_id = fields.Many2one('sn_credit.prelevement', string='Prelevement Reference',

                               index=True, copy=False, readonly=True, default=10000000)
    cuts_ids = fields.One2many('sn_credit.cuts.lines', 'aksat_line_id', string='Enlèvements')


    sequence = fields.Integer(string='Sequence', default=10)
    amount = fields.Float('Montant', required=True)
    day_to_cut = fields.Date('Le jour')
    moi = fields.Integer(string="Mois", required=True, )
    annee = fields.Integer(string="Année", required=True, )
    etat = fields.Selection(string='Etat de pere', related='aksat_id.state')
    state = fields.Selection(string="Etat", selection=[('generated', 'Géneré'),
                                                   ('declared', 'Déclaré'),
                                                   ('validated', 'Validé'),
                                                   ('refused', 'Réfusé'),
                                                   ('postponed', 'Retardé'),
                                                   ('terminated', 'Términé'),
                                                   ],
                             required=False, default='generated' )

    avancement = fields.Integer('Succès',compute='_compute_avancement')

    echecs = fields.Integer('Échecs',compute='_compute_avancement')

    state_parent =fields.Selection('Etat parent',related='aksat_id.state')
    client_ccp_numero = fields.Char('CompteA', related='aksat_id.partner_id.ccp_numero')
    client_ccp_cle = fields.Char('CleA', related='aksat_id.partner_id.ccp_cle')

    client_nom = fields.Char('Nom', related='aksat_id.partner_id.name')
    

    contrat = fields.Char('Contrat', related='aksat_id.contrat.name')
    contrat_ccp_numero = fields.Char('CompteB', related='aksat_id.contrat.ccp_numero')
    contrat_ccp_cle = fields.Char('CleB', related='aksat_id.contrat.ccp_cle')

    date_start = fields.Date('Date Début', related='aksat_id.date_start')
    date_end = fields.Date('Date Fin', related='aksat_id.date_end')
    date_creation = fields.Date('Date Création', related='aksat_id.creation_date')

    nbr_echeance = fields.Integer('Nbr Echéance', related='aksat_id.month_number')
    jour_prelevement = fields.Integer('JourPrel', related='aksat_id.jour')
    mth_traited = fields.Integer('Mois traité', default=0)

    @api.depends('cuts_ids')
    def _compute_avancement(self):
        for hala in self:
            hala.avancement = hala.cuts_ids.search_count([('aksat_line_id','=',hala.id),('c_etat','=','0')])
            hala.echecs = hala.cuts_ids.search_count([('aksat_line_id','=',hala.id),('c_etat','!=','0')])

##################################################################
class NticAksatsReelMonthsLines(models.Model):
    _name = "sn_credit.aksats.mois_reel_sah"
    _description = "retrait reel mensuel des aksats Sah"

    
    aksat_id = fields.Many2one('sn_sales.commandes' )    
    mois_annee = fields.Char(string='Date opération')
    mta_deduit = fields.Float(string='Mta déduit')
##################################################################


class NticAksatsReelMonthsLines(models.Model):
    _name = "sn_credit.aksats.mois_reel"
    _description = "retrait reel mensuel des aksats"
    _auto = False

    id = fields.Integer(string='ref' )
    aksat_id = fields.Integer(string='Aksat Reference' )    
    #annee = fields.Integer("annee")
    mois_annee = fields.Char(string='Date opération')
    #company_id = fields.Many2one('res.company', 'Company')
    mta_deduit = fields.Float(string='Mta déduit')
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
         
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
            SELECT row_number() OVER () as id,
                commande_aksat_line_id AS aksat_id,                
                c_annee::varchar(4) || '-' || LPAD(c_mois::varchar(2), 2, '0') as mois_annee,
	            sum(case c_etat when '0' then c_montant else 0 end ) AS mta_deduit
                FROM sn_credit_cuts_lines                
                GROUP BY commande_aksat_line_id,mois_annee
                ORDER BY mois_annee Desc
              
            )''' % (self._table)
        )

# where  date_trunc('month', current_date - interval '1' month)>TO_DATE(annee_reel::varchar(4) || '-' || LPAD(mois_reel::varchar(2), 2, '0')  || '-01' ,'YYYY-MM-DD')
class NticAksatsR4Retards(models.Model):
    _name = "sn_credit.aksats.mois_retard"
    _description = "retard mensuel des aksats"
    _auto = False

    aksat_id = fields.Integer( string='Aksat Ref.' )
    mois = fields.Integer("mois")
    annee = fields.Integer("annee")
    mois_annee = fields.Char(string='Date opération')
    company_id = fields.Many2one('res.company', 'Company')
    mta_deduit = fields.Float(string='Mta déduit')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
            SELECT row_number() OVER () as id,
                   commande_aksat_line_id AS aksat_id,    
                   mois_reel as mois,
                   annee_reel as annee,   
                   annee_reel::varchar(4) || '-' || LPAD(mois_reel::varchar(2), 2, '0')  as mois_annee,            
                   company_id,
                   sum(case c_etat when '0' then c_montant else 0 end ) AS mta_deduit
            FROM sn_credit_cuts_lines 
            WHERE  date_trunc('month', current_date - interval '1' month)>TO_DATE(annee_reel::varchar(4) || '-' || LPAD(mois_reel::varchar(2), 2, '0')  || '-01' ,'YYYY-MM-DD')
            GROUP BY  company_id,commande_aksat_line_id,annee_reel,mois_reel
            ORDER BY  commande_aksat_line_id,mois_annee DESC
            )''' % (self._table)
        )

 
