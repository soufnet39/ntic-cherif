from odoo import models, fields
import psycopg2

class BlackListWizard(models.TransientModel):
    _name = 'cherif.black_list_wizard'

    related_databases = fields.Char(string="Les annexes", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('related_databases'))
    call_done = fields.Boolean(string='Appel effectué', default=False)
    nbr_called = fields.Integer(string='Nombre de cas trouvé', default=0)
    new_black_clients_ids = fields.One2many('cherif.black_list_details_wizard', 'bl_id', string='Liste des clients ajoutés à la liste noire')


    # @api.multi
    def call_them(self):
        self.call_done = True
        current_db=self.pool.db_name
        databases = self.related_databases.split(',')
        if current_db in databases:
            databases.remove(current_db)
        for db in databases:
            conn_string="dbname='%s' host='db' user=odoo password='odoo' port=5432"
            # try:
            with psycopg2.connect(conn_string%(db)) as connection:
                    cur = connection.cursor()
                    cur.execute("""
                    select name,ccp_numero,ccp_cle,wilaya,user,create_date  FROM public.cherif_black_list
                    """)                                                        
                    rows = cur.fetchall()
                    for row in rows:
                        res=  self.env['cherif.black_list'].search(['&',('ccp_numero','=',row[1]),('ccp_cle','=',row[2])])
                        if not res:
                            bl_id = self.env['cherif.black_list'].create({
                                'name': row[0],
                                'ccp_numero': row[1],
                                'ccp_cle': row[2],
                                'wilaya': row[3],
                                'user': row[4],
                                'create_date': row[5],
                            })
                            self.env['cherif.black_list_details_wizard'].create({
                                'bl_id': self.id,
                                'name': row[0],
                                'ccp_numero': row[1],
                                'ccp_cle': row[2],
                                'wilaya': row[3],
                                'user': row[4]                               
                            })
                           
                      
        return {'type': 'ir.actions.act_window_close'}

class BlackListDetailsWizard(models.TransientModel):
        _name = "cherif.black_list_details_wizard"
        _description = "Liste des clients trouvés dans les annexes"

        bl_id = fields.Many2one('cherif.black_list_wizard', string='Black List in Relation')
       
        name = fields.Char('Client' )
        ccp_numero = fields.Char(string="CCP"  )
        ccp_cle    = fields.Char(string="Clé" )
        wilaya = fields.Char(string="Wilaya" )
        user   = fields.Char(string="Agent" )