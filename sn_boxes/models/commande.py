from odoo import api, models, fields, _

class SnSalesBoxesCommandes(models.Model):
    _inherit = 'sn_sales.commandes'

    payment_ids = fields.One2many('sn_boxes.operations', 'commande_id', string='Paiement', copy=False)
    show_client_payment = fields.Boolean(string="Afficher les paiements",
                               default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                   'sn_boxes.show_client_payment'))
    total_reglement = fields.Float(string='Total Reglements',digits="montant", store=True, compute='_compute_total_reglement')

    amount_rest = fields.Float(string='Reste',digits="montant", compute='_compute_total_reglement', store=True)
    
    @api.depends('payment_ids','commande_lines') #,'amount_ttc'
    def _compute_total_reglement(self):
        #super(SnSalesBoxesCommandes, self)._compute_total_reglement()
        for rec in self:
            tot = 0.0
            for line in rec.payment_ids:
                tot += line.amount
            rec.update({
                'total_reglement': tot,
                'amount_rest': rec.amount_ttc - tot,
                'amount_ttc_sec': rec.amount_ttc - tot,
            })
