from odoo import models, fields, api, _ 
from odoo.exceptions import UserError

import psycopg2
class NticCreditPartner2(models.Model):
    _inherit = 'sn_sales.partner'
    _description = "Credits part of partner"


    prenom = fields.Char(string="Prénom" )
    ccp_numero = fields.Char(string="Numéro CCP" )
    ccp_cle    = fields.Char(string="Clé CCP")

    _sql_constraints = [
        ('ccp_unique', 'unique(ccp_numero,ccp_cle)', 'Les comptes CCP doivent être uniques!'),
    ]

    #def name_get(self):
    @api.depends('name', 'prenom', 'ccp_numero')
    def _compute_display_name(self):        
        #result = []
        for account in self:
            account.display_name = (account.name or '') + ' ' + (account.prenom or '') + ' ' + (account.ccp_numero or '')
            #result.append((account.id, (account.name or '') + ' ' + (account.prenom or '') + ' ' + (account.ccp_numero or '')))
        #return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search((args + ['|', '|', ('name', 'ilike', name), ('prenom', 'ilike', name), ('ccp_numero', 'ilike', name)]),
                               limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()

    @api.model
    def create(self, vals):         
        if vals.get('ccp_numero'):
            self.verifa(vals['ccp_numero'])            
        return super(NticCreditPartner2, self).create(vals) 
   
    def write(self, vals):  
        if vals.get('ccp_numero'):
            self.verifa(vals['ccp_numero'])   
        return super(NticCreditPartner2, self).write(vals) 

    def verifa(self,ccp):
        current_db=self.pool.db_name
        dbs1=['oran','saida','baraki','yasmine']
        dbs2=['mosta','blida','ouargla']
        dbs= dbs1 if (current_db in dbs1) else dbs2 if (current_db in dbs2) else []

        if len(dbs)>1:
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

    
