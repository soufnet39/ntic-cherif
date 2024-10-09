from odoo import api, fields, models

class NticCherifSuppliers(models.Model):
    _name = "cherif_suppliers.suppliers"
    #_inherit = [ 'mail.thread', 'mail.activity.mixin']
    _description = "Suivi des fournisseurs"
    _order = 'name_supplier asc'

   

    code_supplier = fields.Char('Code Fournisseur')
    name_supplier = fields.Char('Nom Fournisseur')

    achat_ids = fields.One2many('cherif_suppliers.suppliers_achats', 'supplier_id', string='Achats')  
    reglement_ids = fields.One2many('cherif_suppliers.suppliers_reglements', 'supplier_id', string='Réglements')    
    total_achat = fields.Float('Total Achats', compute='_compute_total', digits="montant",store=True,readonly=True )
    total_reglement = fields.Float('Total Réglements', compute='_compute_total', digits="montant",store=True,readonly=True)
    reste = fields.Float('Reste à régler', compute='_compute_total', digits="montant")

    @api.depends('achat_ids.montant_achat','reglement_ids.montant_reglement')
    def _compute_total(self):
        for suplier in self:
            tot_ach = 0
            for achat in suplier.achat_ids:
                tot_ach += achat.montant_achat
            suplier.total_achat = tot_ach
            tot_reg = 0
            for reglement in suplier.reglement_ids:
                tot_reg += reglement.montant_reglement
            suplier.total_reglement = tot_reg
            suplier.reste = tot_ach - tot_reg


class NticCherifSuppliersAchat(models.Model):
    _name = "cherif_suppliers.suppliers_achats"

    supplier_id = fields.Many2one('cherif_suppliers.suppliers', string='Fournisseur Ref',
                                ondelete='cascade',
                                index=True,copy=False, readonly=True)
    name_supplier = fields.Char(related='supplier_id.name_supplier',store=True)

    ref_achat = fields.Char('Numéro Facture')
    date_achat = fields.Date('Date Facture')
    montant_achat =  fields.Float("Montant", digits="montant")

class NticCherifSuppliersReglements(models.Model):
    _name = "cherif_suppliers.suppliers_reglements"

    supplier_id = fields.Many2one('cherif_suppliers.suppliers', string='Fournisseur Ref',
                                ondelete='cascade',
                                index=True,copy=False, readonly=True)
    
    date_reglement = fields.Date('Date Réglement',default=fields.Date.today())
    montant_reglement =  fields.Float("Montant", digits="montant")
    observation = fields.Char('Observation')