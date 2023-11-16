from odoo import models, fields, tools,api

class NticCommandes_purchases(models.Model):
    _inherit = "sn_sales.commandes"

    # partner_id_suppliers = fields.Many2one('sn_sales.partner', string='Fournisseur', track_visibility='always',   track_sequence=1,    index=True  )
    # tarification_supplier = fields.Selection('Tarification', related='partner_id_suppliers.tarification')

    ref_facture_achat_source = fields.Char(string="Num. Réference"    )
 
    def print_purchase(self):
        return self.env.ref('sn_purchases.action_report_purchase').report_action(self)

class NticAchatCommandesLines(models.Model):
    _inherit = "sn_sales.commande.lines"

   # price_achat = fields.Float('Prix Achat', required=True, default=0.0)
   # partner_id_suppliers = fields.Many2one(related='commande_id.partner_id_suppliers', store=True, string='Supplier',    readonly=False)

    ######################################################
    # overwitten in its turn at cherif module if installed #
    ######################################################
    @api.onchange('product_id')
    def affect_name_to_designation(self):
        if not self.product_id.id:
            return

        price = 66666
        libelle = ''
        if self.commande_id.tarification=='standard' and self.commande_id.operation_type=='purchase':
            price = self.product_id.purchase_price
            self.price_changed = False
            self.price_touched = False
        if self.commande_id.tarification=='standard' and self.commande_id.operation_type=='command':
            price = self.product_id.default_price
            self.price_changed = False
            self.price_touched = False
        if self.commande_id.tarification == 'special':
            if self.commande_id.list_prix and self.product_id.pricelist_item_ids:
                for prix in self.product_id.pricelist_item_ids:
                    if prix.pricelist_id.id == self.commande_id.list_prix.id:
                        price = prix.fixed_price
                        libelle= prix.pricelist_id.name

        self.price_unit=price
        self.price_list_libelle=libelle
        self.name = self.product_id.name

