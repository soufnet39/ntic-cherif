from odoo import  fields, models, _
import psycopg2

class cherif_suppliers_wizard(models.TransientModel):
    _name = "cherif_suppliers.suivi_wizard"
    _description = "Wizard to traite suppliers operations"

    related_databases = fields.Char(string="Les annexes", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('suppliers_related_databases'))
    last_call = fields.Char(string="Derniere synchronisation", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('suppliers_last_call'))
    sync_done = fields.Boolean(string="Synchronisation effectuée", default=False)
    anomalies = fields.Text(string="Anomalies")
    new_operation_ids = fields.One2many('cherif_suppliers.suivi_details_wizard', 'suivi_id', string='Nouvelles opérations')

    def synca(self):
        self.last_call = fields.Datetime.now()
        self.env['ir.config_parameter'].sudo().set_param('suppliers_last_call', fields.Datetime.now())
        self.sync_done = True


        # List of databases to sync
        databases = self.related_databases.split(',')
        for db in databases:
            conn_string="dbname='%s' host='db' user=odoo password='odoo' port=5432"
            # try:
            with psycopg2.connect(conn_string%(db)) as connection:
                    cur = connection.cursor()
                    cur.execute("""
                    select concat(w.code,'/',p.name) as name,f.name as supplier ,f.ref, p.amount_ttc,p.confirmation_date as date From (SELECT name,company_id,partner_id,amount_ttc,confirmation_date  FROM public.sn_sales_commandes  where operation_type='purchase') p
                    left join public.res_company rc on rc.id = p.company_id
                    left join public.sn_base_wilayates w on rc.wilaya_id =w.id
                    left join public.sn_sales_partner f on f.id=p.partner_id
                    """)
                    rows = cur.fetchall()
                    for row in rows:
                        res=  self.env['cherif_suppliers.suppliers'].search([('code_supplier','=',row[2])])
                        if not res:
                            supl_id = self.env['cherif_suppliers.suppliers'].create({
                                'code_supplier': row[2],
                                'name_supplier': row[1],
                            })
                            self.env['cherif_suppliers.suppliers_achats'].create({
                                'supplier_id': supl_id.id,
                                'ref_achat': row[0],
                                'montant_achat': row[3],
                                'date_achat': row[4]
                            })
                        else:
                            is_there_achat = self.env['cherif_suppliers.suppliers_achats'].search([('ref_achat','=',row[0])])
                            if not is_there_achat:
                                self.env['cherif_suppliers.suppliers_achats'].create({
                                    'supplier_id': res[0].id,
                                    'ref_achat': row[0],
                                    'montant_achat': row[3],
                                    'date_achat': row[4]
                                })
                                self.env['cherif_suppliers.suivi_details_wizard'].create({
                                    'suivi_id': self.id,
                                    'name': row[0],
                                    'code_supplier': row[2],
                                    'name_supplier': row[1],
                                    'total_achat': row[3],
                                    'date_achat': row[4],
                                })
                            else:
                                if is_there_achat[0].montant_achat != row[3]:
                                    is_there_achat[0].montant_achat = row[3]
                                    self.env['cherif_suppliers.suivi_details_wizard'].create({
                                        'suivi_id': self.id,
                                        'name': row[0],
                                        'code_supplier': row[2],
                                        'name_supplier': row[1],
                                        'total_achat': row[3],
                                        'date_achat': row[4],
                                    })

            # except:
            #     print('database does %s not exist'%(db)) 
            #     continue
        


        
    class cherif_suppliers_wizard(models.TransientModel):
        _name = "cherif_suppliers.suivi_details_wizard"
        _description = "Details of operations"

        suivi_id = fields.Many2one('cherif_suppliers.suivi_wizard', string='Suivi')
        name= fields.Char('Reference') # add wilaya to achat num ex:  39/ACH/0022
        code_supplier = fields.Char('Code Fournisseur')
        name_supplier = fields.Char('Nom Fournisseur')        
        total_achat = fields.Float('Total Achats', digits="montant")
        date_achat = fields.Date('Date',)

        

