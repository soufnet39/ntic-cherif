from odoo import models, fields, api, _
from odoo.exceptions import UserError
import psycopg2

class NticCherifCommande(models.Model):
    _inherit = "sn_sales.partner"
    
    date_naissance = fields.Date(string='Date de naissance', copy=False)
    lieu_naissance = fields.Char(string="Lieu de naissance")
    pere = fields.Char(string="Nom du père")
    mere = fields.Char(string="Nom de la mère")
    nom_epous = fields.Char(string="Nom Epous")

    # function:     // exist already
    employeur = fields.Char(string="Employeur")
    identity_card_number = fields.Char(string="Pièce d'identité n°")
    identity_card_date = fields.Date(string="PI délivré le")
    identity_card_place = fields.Char(string="PI délivré à")
    
    commandes_ids = fields.One2many('sn_sales.commandes','partner_id')
    commandes_count = fields.Integer(string='Nombre de commandes', compute='_compute_commandes_count', store=True)
    _is_cherif_boss = fields.Boolean(compute='_compute_is_cherif_boss')
    # can_buy_more : can the same client buy an other time 
    can_buy_more = fields.Boolean(string='Peut acheter une autre fois', default=True)
    # sensitive data state is: [false:read only / true:writable] (name, ccp_numero, ccp_cle)
    # the default state is True, this can be changed to False by the admin or if the last command of this client deppassed 24 hours
    sensitive_data_state_is_changeable = fields.Boolean(string='Sensitive Data State', default=True)
    @api.depends('commandes_ids')
    def _compute_commandes_count(self):
        for partner in self:
            partner.commandes_count = len(partner.commandes_ids)

    @api.depends_context('uid')
    def _compute_is_cherif_boss(self):
        is_boss = self.env.user.has_group('cherif.cherif_boss')
        for partner in self:
            partner._is_cherif_boss = is_boss

    # function:     // overwrite already existing funtion in sn_credit
    def verifa(self,ccp):
        res=  self.env['cherif.black_list'].search([('ccp_numero','=',ccp)])
        if res:
            raise UserError(_('Ce code CCP est sur la liste noire'))    

        current_db=self.pool.db_name
        r_dbs=self.env['ir.config_parameter'].sudo().get_param('related_databases')
        dbs= r_dbs.split(',')
        if (current_db in dbs) and len(dbs)>1:
            dbs.remove(current_db)
            for db in dbs:
                conn_string="dbname='%s' host='db' user=odoo password='odoo' port=5432"
                # try:
                with psycopg2.connect(conn_string%(db)) as connection:
                    cur = connection.cursor()
                    cur.execute("SELECT * FROM public.sn_sales_partner where ccp_numero='%s'"%(ccp))
                    rows = cur.fetchall()
                    if rows:
                        raise UserError(_('Ce code CCP exist déjà à :%s'%(db))) 
                # except:
                #     print('database does %s not exist'%(db)) 
                #     loop
        return True
    def let_him_buy_more(self):
        self.can_buy_more = True
        return True
    def stop_buy_more(self):
        self.can_buy_more = False
        
    
   