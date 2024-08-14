from odoo import  fields, models, _
import psycopg2
from odoo.exceptions import UserError


class search_client_wizard(models.TransientModel):
    _name = "cherif_suppliers.search_client"
    _description = "Wizard to Shearch Client on all feliales"

    name2search = fields.Char(string='Nom du Client ou CCP', required=True)
    client_ids = fields.One2many('cherif_suppliers.search_client.details','search_id', string='Clients')

    def look4client(self):

        dbs=self.env['ir.config_parameter'].sudo().get_param('related_databases')
        databases = dbs.split(',')
        self.client_ids.unlink()
        for db in databases:
            conn_string="dbname='%s' host='localhost' user=smail password='root' port=5432"
            # conn_string="dbname='%s' host='db' user=odoo password='odoo' port=5432"
            # try:
            with psycopg2.connect(conn_string%(db)) as connection:
                cur = connection.cursor()
                cur.execute("""
                    SELECT cmd.name, cmd.confirmation_date as dte,clnt.name, clnt.ccp_numero,cmd.amount_ttc,cmd.month_number ,cmd.monthly_amount  FROM public.sn_sales_commandes as cmd 
                    left join public.sn_sales_partner as clnt 
                    on cmd.partner_id=clnt.id
                    where cmd.operation_type = 'command' and (lower(clnt.name) LIKE %s OR clnt.ccp_numero LIKE %s) 
                    """, ('%' + self.name2search.lower() + '%', '%' + self.name2search + '%'))
                rows = cur.fetchall()
                if len(rows)>0:
                    for row in rows:
                        self.env['cherif_suppliers.search_client.details'].create({
                            'search_id': self.id,
                            'filiale': db,
                            'cmd_name': row[0],
                            'cmd_date': row[1],
                            'client_name': row[2],
                            'client_ccp': row[3],
                            'mta': row[4],
                            'month_number': row[5],
                            'monthly_amount': row[6]
                        })                    


class search_client_details_wizard(models.TransientModel):
    _name = "cherif_suppliers.search_client.details"
    _description = "Details of clients search"

    search_id = fields.Many2one('cherif_suppliers.search_client', string='Search Client')
    filiale= fields.Char('Filiale')
    cmd_name= fields.Char('Commande')
    client_name= fields.Char('Client')
    client_ccp= fields.Char('CCP')
    mta= fields.Float('Montant', digits="montant")
    cmd_date= fields.Date('Date')
    month_number=fields.Integer('Nbr Mois')
    monthly_amount =fields.Float('Par Mois', digits="montant")
       
    

