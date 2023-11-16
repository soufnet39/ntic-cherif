from odoo import models, fields, tools

class NticEtat104Lines(models.Model):
    _name = "sn_invoices.etat_104"
    _description = "Etat 104"
    _order = 'nom asc'
    _auto = False

    id_client = fields.Integer(  string='Id',  readonly=True  )
    annee = fields.Integer(  string='Anneé',  readonly=True  )    
    nom = fields.Char(  string='Nom',  readonly=True  )    
    adresse = fields.Char(  string='Adresse',  readonly=True  )    
    reg_com  = fields.Char(  string='Reg. Com.',  readonly=True  )    
    mat_fisc  = fields.Char(  string='Mat.Fisc.',  readonly=True  )    
    art_imp  = fields.Char(  string='Art. Imp.',  readonly=True  )    
    nis  = fields.Char(  string='Nis',  readonly=True  )    
    #nif  = fields.Char(  string='Nif',  readonly=True  )    
    phone = fields.Char(  string='Phone',  readonly=True  )    
    mobile = fields.Char(  string='Mobile',  readonly=True  ) 
    ht = fields.Float(  string='HT', digits=(16, 2) , readonly=True  ) 
    timbre = fields.Float(  string='Timbre', digits=(16, 2) , readonly=True  ) 
    tva = fields.Float(  string='TVA', digits=(16, 2) , readonly=True  ) 
    ttc  = fields.Float(  string='TTC', digits=(16, 2) , readonly=True  ) 
  

    ## Overwritten in Albelt
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
            select row_number() OVER () as id, id as id_client,a.annee,name as nom,address as adresse,reg_com,mat_fisc,art_imp,nis,
            phone,mobile, a.ht,a.timbre,a.tva, a.ttc from sn_sales_partner as p 
            inner join
            (select  extract(year from confirmation_date) as annee, partner_id,sum(amount_ht_signed) as ht, sum(amount_tva_signed) as tva, sum(amount_timbre_signed) as timbre,sum(amount_ttc_signed) as ttc 
			 from sn_invoices_invoices where state  in ( 'confirmed','avoir' )  group by extract(year from confirmation_date) , partner_id) as a
            on p.id=a.partner_id 
            )''' % (self._table)
        )