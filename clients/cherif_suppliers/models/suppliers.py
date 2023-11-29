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
    total_achat = fields.Float('Total Achats', compute='_compute_total_achats', digits="montant",store=True,readonly=True )
    total_reglement = fields.Float('Total Réglements', compute='_compute_total_reglements', digits="montant",store=True,readonly=True)
    reste = fields.Float('Reste à régler', compute='_compute_reste', digits="montant",store=True,readonly=True)

    @api.depends('achat_ids')
    def _compute_total_achats(self):
        for suplier in self:
            tot = 0
            for achat in suplier.achat_ids:
                tot += achat.montant_achat
            suplier.total_achat = tot

    @api.depends('reglement_ids')
    def _compute_total_reglements(self):
        for suplier in self:
            tot = 0
            for reglement in suplier.reglement_ids:
                tot += reglement.montant_reglement
            suplier.total_reglement = tot

    @api.depends('total_achat','total_reglement')
    def _compute_reste(self):
        for suplier in self:
            suplier.reste = suplier.total_achat - suplier.total_reglement


class NticCherifSuppliersAchat(models.Model):
    _name = "cherif_suppliers.suppliers_achats"

    supplier_id = fields.Many2one('cherif_suppliers.suppliers', string='Fournisseur Ref',
                                ondelete='cascade',
                                index=True,copy=False, readonly=True)
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