from odoo import models, fields,api,_
from odoo.exceptions import UserError
import psycopg2

class NticCherifBlackList(models.Model):
    _name = "cherif.black_list"    
    _description = "Liste noire des clients"
    _order = 'create_date asc'

    name = fields.Char('Client',required=True)
    card_id = fields.Char('Identité')
    ccp_numero = fields.Char(string="CCP",required=True )
    ccp_cle    = fields.Char(string="Clé",required=True)
    wilaya = fields.Char(string="Wilaya",readonly=True)
    motif = fields.Char(string="Motif",)
    agent   = fields.Char(string="Agent",readonly=True)
    _sql_constraints = [
        ('ccp_unique', 'unique(ccp_numero,ccp_cle)', _('Les comptes CCP doivent être uniques même à la list noire!')),
    ]
    
    @api.model
    def create(self, vals):         
        vals['ccp_numero'] = str(int(vals.get('ccp_numero')))
        chosen_company_id = self.env.user.company_id    
        vals['wilaya'] = chosen_company_id.wilaya_id.name     
        vals['agent'] = self.env.user.name

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
                    cur.execute("INSERT into public.cherif_black_list (name,ccp_numero,ccp_cle,wilaya,motif,agent) VALUES ('%s','%s','%s','%s','%s','%s')"%(vals['name'],vals['ccp_numero'],vals['ccp_cle'],vals['wilaya'],vals['motif'],vals['agent']))
                    # raise UserError(_('Error lors de l insersion à:%s'%(db))) 

        return super(NticCherifBlackList, self).create(vals)
            