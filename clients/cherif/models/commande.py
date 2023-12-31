from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class NticCherifCommandes(models.Model):
    _inherit = "sn_sales.commandes"

    def _default_related_id(self):        
        first_record = self.env['sn_sales.pricelist'].search([], limit=1)
        return first_record.id if first_record else False
    pricelist_id = fields.Many2one(comodel_name="sn_sales.pricelist", string="Price by aksat methods",default=_default_related_id,store=True)
     
    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        if self.pricelist_id:
            self.month_number = self.pricelist_id.numberOfMonths
    
    
    def unlink(self):
        # import wdb; wdb.set_trace()

        if not self.env.user.has_group('sn_sales.sn_sales_manager'):
            raise UserError(_("Vous n'êtes pas autorisé de supprimer ce bon. consulter votre responsable."))
        return super(NticCherifCommandes, self).unlink()

    

    # @api.model
    # def write(self, vals):
    #     raise UserError(_("You are not allowed to modify this record."))

    #     is_purchase_user = self.env.ref("sn_purchases.sn_purchases_user", raise_if_not_found=False)
    #     if is_purchase_user and self.state in ['confirmed','canceled']:
    #         raise UserError(_("You are not allowed to modify this record."))
        
    #     return super(NticCreditsCommande, self).write(vals)
   
class NticCherifCommandesLines(models.Model):
    _inherit = "sn_sales.commande.lines"

    def _default_pricelist_ids(self):        
        records = self.env['sn_sales.pricelist.item'].search([('product_id', '=', self.product_id.id)])
        return [ r.id for r in records] if records else False
    
    # to use at purchase order
    pricelist_item_ids = fields.One2many('sn_sales.pricelist.item', 'product_id', 'Pricelist Items',related='product_id.pricelist_item_ids',readonly=False ) #

    # @api.onchange('pricelist_item_ids.price_of_month')
    # def _onchange_price_of_month(self,vals):
    #     raise UserError(vals)
    #     if self.pricelist_item_ids:
    #         self.pricelist_item_ids.fixed_price = self.pricelist_item_ids.price_of_month*2#self.pricelist_id.numberOfMonths
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
            price = self.product_id.purchase_price
            self.price_changed = False
            self.price_touched = False
        if self.commande_id.tarification=='standard' and self.commande_id.operation_type=='command':
            if self.product_id.pricelist_item_ids:         
                for prix in self.product_id.pricelist_item_ids:
                    if prix.pricelist_id.id == self.commande_id.pricelist_id.id:
                        price = prix.fixed_price
                        libelle= prix.pricelist_id.name       
                
                 
                #self.price_changed = False
                #self.price_touched = False
        if self.commande_id.tarification == 'special':
            if self.commande_id.list_prix and self.product_id.pricelist_item_ids:
                for prix in self.product_id.pricelist_item_ids:
                    if prix.pricelist_id.id == self.commande_id.list_prix.id:
                        price = prix.fixed_price
                        libelle= prix.pricelist_id.name

        self.price_unit=price
        self.price_list_libelle=libelle
        self.name = self.product_id.name