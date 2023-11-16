from odoo import api, models, fields, _
from datetime import datetime
from odoo.exceptions import ValidationError, RedirectWarning, UserError

class BoxesOperationsModule(models.Model):
    _name = 'sn_boxes.operations'
    _description = 'Ntic Boxes Opération'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_action desc, id desc'

    operation = fields.Selection(string="Opération", selection=[
                                ('paiement', 'Recette'),
                                ('expense', 'Dépense'),
                                ('retour', 'Retour'),
                                ('transfer', 'Transfer'),
                                ('virement', 'Virement'),
                                ('versement', 'Versement'),
                                ('reception', 'Encaissement'),
                                ('purchase', 'Achat'),
                                ('degagement', 'Décaissement'),], default='reception'
                            )

    name = fields.Char(string="Motif", required=True, )
    user_id = fields.Many2one('res.users', string='Vendeur',default=lambda self: self.env.user ) # ,track_visibility='onchange', track_sequence=2 
    boxe = fields.Many2one(comodel_name="sn_boxes.boxes", string="Compte", required=True, )
    amount = fields.Float(string="Montant",  required=True, track_visibility='onchange', )
    amount_done = fields.Float(string='Montant', compute='_amount_done', store='true')
    mode = fields.Selection(string="Mode", selection=[
                            ('sold', 'Espèce'),
                            ('bank', 'Chèque'),
                            ('virement', 'Virement'),
                            ('versement', 'Versement'),
                            ],
                            required=True, default='sold')
    # if mode = bank -> reference is (cheque info)
    # if mode = paiement -> reference is (bc num)

    reference = fields.Char(string="Reference", required=False, )
    commande_id = fields.Many2one('sn_sales.commandes', string='Commande', copy=False, readonly=True, )
    #purchase_id = fields.Many2one('sn_purchases.order', string='Achat', copy=False, readonly=True, )

    partner_id = fields.Many2one('sn_sales.partner', string="Client/Fournis.",  domain=[('is_customer', '=', True)] )
    
    representant = fields.Char(   string='Répresentant'  )
    is_printed = fields.Boolean(  string='Imprimé?'  )
    
    

    date_action = fields.Date(string="Date Opération", required=True, default=lambda self:fields.Date.today())
    date_echeance = fields.Date(string="Date Chèque", default=lambda self:fields.Date.today())

    etat_bancaire = fields.Selection(string="Etat Bancaire", selection=[
                            ('with_us', 'Chez Nous'),
                            ('in_circulation', 'En Circulation'),
                            ('unpaid', 'Impayé'),
                            ('paid', 'Payé'),
                            ('canceled', 'Annulé'),],
                             )

    date_valeur = fields.Date(string="Date pose", required=False, default=lambda self:fields.Date.today())
    date_encaissement = fields.Date(string="Date Encais.", required=False, default=lambda self:fields.Date.today())

    # debit (-) , credit (+)
    sens = fields.Selection(string="Sens", selection=[
                                ('debit', 'Décaissement'),
                                ('credit', 'Encaissement'), ],
                                required=True, )



    locked = fields.Boolean(string="Verrouillé", default=False)

    wilaya = fields.Many2one(related='boxe.wilaya_id', string="Wilaya" , store=True)
    region = fields.Many2one(related='boxe.region', string="région", store=True)

    sold_boxe = fields.Float(related='boxe.sold_boxe')
    # sold_client = fields.Float(related='partner_id.sold_client')

    # TODO:: MUST BE REVISED
    # @api.constrains('amount')
    # def _check_sold(self):
    #     for v in self:
    #         if v.amount<=0:
    #             raise ValidationError(_('Pas de somme NULLE ou NEGATIFE!!.'))

    @api.constrains('amount', 'sold_boxe')
    def _check_difference(self):
        for rec in self:
            if rec.sold_boxe<0:
                raise ValidationError(_('Desole, On peut pas decaisser plus que le sold du compte.'))

    @api.depends('amount')
    def _amount_done(self):
        for rec in self:
            rec.amount_done = rec.amount if rec.sens=='credit' else -1*rec.amount

    # the bellow functin duplicated a in sn_boxes.boxes

    def sold_boxe_function(self):
        tree_view_id = self.env.ref('sn_boxes.sn_boxes_operations_list_view').ids
        search_view_id = self.env.ref('sn_boxes.sn_boxes_operations_search_view').ids
        form_view_id = self.env.ref('sn_boxes.sn_boxes_operations_form_view').ids
        # TODO:: search_view_id don't work properly
        return {
            'views': [[tree_view_id, 'tree'], [form_view_id, 'form'], [search_view_id, 'search']],
            'name': _('Opérations'),
            'view_mode': 'tree',
            'res_model': 'sn_boxes.operations',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [("boxe", '=', self.boxe.id)]
        }

    # the bellow functin duplicated a in sn_sales.partner (sn_boxes)

    def sold_client_function(self):
        tree_view_id = self.env.ref('sn_boxes.sn_boxes_operations_list_view').ids
        search_view_id = self.env.ref('sn_boxes.sn_boxes_operations_search_view').ids
        form_view_id = self.env.ref('sn_boxes.sn_boxes_operations_form_view').ids
        # TODO:: search_view_id don't work properly
        return {
            'views': [[tree_view_id, 'tree'], [form_view_id, 'form'], [search_view_id, 'search']],
            'name': _('Opérations'),
            'view_mode': 'tree',
            'res_model': 'sn_boxes.operations',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [("partner_id", '=', self.partner_id.id)]
        }

    def print_bon_caisse(self):
        return self.env.ref('sn_boxes.bon_caisse_report').report_action(self)


