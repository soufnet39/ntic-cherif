from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
import datetime
import psycopg2
class NticCherifCommandes(models.Model):
    _inherit = "sn_sales.commandes"

    def _default_related_id(self):        
        first_record = self.env['sn_sales.pricelist'].search([], limit=1)
        self.month_number = first_record.numberOfMonths
        return first_record.id if first_record else False
    pricelist_id = fields.Many2one("sn_sales.pricelist", string="Price by aksat methods",default=_default_related_id,store=True) #
    after24hours = fields.Boolean('After24Hours')
    dossier_org = fields.Many2one("cherif.dossierorg", string="Dossier origine") 
                                  
    def check24hours(self):  # this function is fired only from schedeled action       
            yesterday = fields.datetime.now() - datetime.timedelta(days=1)
            records_to_update = self.env['sn_sales.commandes'].search([('create_date', '<', yesterday),('amount_ttc','!=',0),('after24hours','=',False),('operation_type','=','command')])
            clients_ids = []
            for rec in records_to_update:
                clients_ids.append(rec.partner_id.id)
                rec.partner_id.update({'sensitive_data_state_is_changeable':False})
                rec.after24hours = True
            # update the client table set sensitive_data_state_is_changeable to False where id not in clients_ids and sensitive_data_state_is_changeable is True
            self.env['sn_sales.partner'].search([('id', 'not in', clients_ids),('sensitive_data_state_is_changeable','=',True)]).update({'sensitive_data_state_is_changeable':False})
    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        if self.pricelist_id:
            self.month_number = self.pricelist_id.numberOfMonths

    @api.model
    def create(self, vals):   
        if 'commande_lines' in vals.keys():
                for line in vals['commande_lines']: 
                    if line[2]!=False and 'price_total' in line[2].keys():
                         if line[2]['price_total'] == 0:
                            raise UserError(_("Vous ne pouvez pas ajouter une ligne avec un prix OU quantité nulle"))
        return super(NticCherifCommandes, self).create(vals)
             
    def write(self, vals):   
            if self.operation_type == 'command' and self.partner_id.can_buy_more==True:
                self.partner_id.update({'can_buy_more':False})
            if 'commande_lines' in vals.keys():               
                # listnodouble=[]
                # for rec in self.commande_lines.product_id.ids:
                #   if rec in listnodouble:
                #     raise UserError(_("Il exist un article en double")) 
                #   else:
                #     listnodouble.append(rec) 

                for line in vals['commande_lines']: 
                    if line[2]!=False and 'price_total' in line[2].keys():
                         if line[2]['price_total'] == 0:
                            raise UserError(_("Vous ne pouvez pas ajouter une ligne avec un prix OU quantité nulle"))
            return super(NticCherifCommandes, self).write(vals)


    def unlink(self):
        if not self.env.user.has_group('sn_sales.sn_sales_manager') and self.after24hours:
            raise UserError(_("Vous n'êtes pas autorisé de supprimer ce bon. consulter votre responsable."))
        if self.operation_type == 'purchase':
            # conn_string="dbname='eloued' host='localhost' user=smail password='root' port=5432"
            conn_string="dbname='ouargla' host='db' user=odoo password='odoo' port=5432"
            codew = self.env.company.wilaya_id.code
            # try:
            with psycopg2.connect(conn_string) as connection:
                    cur = connection.cursor()
                    qr = f"select  * from public.cherif_suppliers_suppliers_achats where ref_achat ilike '%{codew}/{self.name}%' "
                    cur.execute(qr)
                    rows = cur.fetchall()
                    if rows:
                        raise UserError("Vous ne pouvez pas supprimer ce bon. Il est classé avec les achats, ")

        return super(NticCherifCommandes, self).unlink(not self.after24hours)

    

    def make_it_over24hours(self):
        self.after24hours=True
    def make_it_not_over24hours(self):
        self.after24hours=False

    def print_with_sales_price(self):
        return self.env.ref('cherif.action_report_purchase_with_sales_price').report_action(self)

    @api.onchange('partner_id')
    def _partner_changed(self):
        if self.operation_type == 'command' and not self.env.user.has_group('cherif.cherif_overpass_clients'):
            if self.partner_id:
                if not (self.partner_id.can_buy_more or False):
                    raise UserError(_("Ce client ne peut pas acheter une autre fois"))                
                

class NticCherifCommandesLines(models.Model):
    _inherit = "sn_sales.commande.lines"

    def _default_pricelist_ids(self):        
        records = self.env['sn_sales.pricelist.item'].search([('product_id', '=', self.product_id.id)])
        return [ r.id for r in records] if records else False
    
    # to use at purchase order
    pricelist_item_ids = fields.One2many('sn_sales.pricelist.item', 'product_id', 'Pricelist Items',related='product_id.pricelist_item_ids',readonly=False ) #
    display_date = fields.Date(related='commande_id.display_date')
    ########################################################
    # overwrite sales + purchases same module        #
    ########################################################
    
    @api.onchange('product_id')
    def affect_name_to_designation(self):
        if not self.product_id.id:

            return
        price = 0
        libelle = ''
        if self.commande_id.tarification=='standard' and self.commande_id.operation_type=='purchase':
            # ids = [ x.product_id.id for x  in self.commande_id.commande_lines]
            # if self.product_id.id in ids[:-1]:
            #     raise Warning(_("Ce produit est déjà affecté à cette commande."))
            price = self.product_id.purchase_price
            self.price_changed = False
            self.price_touched = False
            
            
            
        if self.commande_id.tarification=='standard' and self.commande_id.operation_type=='command':
            if self.product_id.pricelist_item_ids:         
                for prix in self.product_id.pricelist_item_ids:
                    if prix.pricelist_id.id == self.commande_id.pricelist_id.id:
                        price = prix.fixed_price
                        libelle= prix.pricelist_id.name  

        self.price_unit=price
        self.price_list_libelle=libelle
        self.name = self.product_id.name


    @api.onchange('pricelist_item_ids')    
    def _onchange_price_of_month(self):  
        if self.commande_id.operation_type=='purchase' and self.price_changed:        
            if len(self.pricelist_item_ids) == 0:
                return    
            for rec in self.pricelist_item_ids:
                if rec.pricelist_id.numberOfMonths!=0 and rec.price_of_month>0:
                    rec.fixed_price = rec.price_of_month*rec.pricelist_id.numberOfMonths
                elif rec.pricelist_id.numberOfMonths!=0 and rec.fixed_price>0:
                    rec.price_of_month = rec.fixed_price/rec.pricelist_id.numberOfMonths
        
    
    @api.onchange('price_unit')
    def on_change_price_unite(self):
            if self.product_id and self.commande_id.operation_type=='purchase'  :
                self.product_id.purchase_price = self.price_unit                
                if self.price_changed:
                    for rec in self.pricelist_item_ids:
                        rec.fixed_price = self.price_unit*(1+rec.taux/100)
                        if rec.pricelist_id.numberOfMonths!=0:
                            rec.price_of_month = rec.fixed_price/rec.pricelist_id.numberOfMonths 
                self.price_changed = True

 
                