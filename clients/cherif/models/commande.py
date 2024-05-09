from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
import datetime

class NticCherifCommandes(models.Model):
    _inherit = "sn_sales.commandes"

    def _default_related_id(self):        
        first_record = self.env['sn_sales.pricelist'].search([], limit=1)
        return first_record.id if first_record else False
    pricelist_id = fields.Many2one("sn_sales.pricelist", string="Price by aksat methods",default=_default_related_id,store=True) #
    after24hours = fields.Boolean('After24Hours')

    
    def check24hours(self):        
            yesterday = fields.datetime.now() - datetime.timedelta(days=1)
            records_to_update = self.env['sn_sales.commandes'].search(['&',('create_date', '<', yesterday),('amount_ttc','!=',0)])
            records_to_update.write({'after24hours': True})
     
    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        if self.pricelist_id:
            self.month_number = self.pricelist_id.numberOfMonths
    
    
    def unlink(self):
        if not self.env.user.has_group('sn_sales.sn_sales_manager'):
            raise UserError(_("Vous n'êtes pas autorisé de supprimer ce bon. consulter votre responsable."))
        return super(NticCherifCommandes, self).unlink()

    

    def make_it_over24hours(self):
        self.after24hours=True
    def make_it_not_over24hours(self):
        self.after24hours=False

class NticCherifCommandesLines(models.Model):
    _inherit = "sn_sales.commande.lines"

    def _default_pricelist_ids(self):        
        records = self.env['sn_sales.pricelist.item'].search([('product_id', '=', self.product_id.id)])
        return [ r.id for r in records] if records else False
    
    # to use at purchase order
    pricelist_item_ids = fields.One2many('sn_sales.pricelist.item', 'product_id', 'Pricelist Items',related='product_id.pricelist_item_ids',readonly=False ) #

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
            ids = [ x.product_id.id for x  in self.commande_id.commande_lines]
            if len(list(set(ids))) < len(ids):
                raise Warning(_("Ce produit est déjà affecté à cette commande."))
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

 
                