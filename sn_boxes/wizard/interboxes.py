from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime


class wizInterBoxes(models.TransientModel):
    _name = 'sn_boxes.interboxes'
    _description = 'transfert de monnais '


    note = fields.Char(string="Déscription", required=False )
    date_transfert = fields.Date(string="Date de transfert", required=False, default=fields.Date.to_string(datetime.now()) )
    state = fields.Boolean(string="Status", default=False)
    boxe_id_from = fields.Many2one(comodel_name="sn_boxes.boxes", string="Compte depart", required=True, )
    boxe_id_to = fields.Many2one(comodel_name="sn_boxes.boxes", string="Compte destination", required=True, )

    sold_from= fields.Float(related='boxe_id_from.sold_boxe')

    # causses trouble when added
    # sold_to= fields.Float(related='boxe_id_to.sold_boxe')

    amount = fields.Float(string="Montant",  required=True, )

    @api.constrains('boxe_id_from', 'boxe_id_to','amount')
    def _constrain_2boxes(self):
        if self.boxe_id_from == self.boxe_id_to:
            raise ValidationError('Compte depart et Compte destination sont identiques')
        if self.amount<=0:
            raise ValidationError('On transfert pas des sommes nulles!')
        if self.amount>self.sold_from:
            raise ValidationError(_('Desole, On peut pas transferer une somme plus que le sold du compte source.'))


    def do_transfert(self):
        obj = self.env['sn_boxes.operations']
        recu = obj.create({
            'operation': 'transfer',
            'name': 'Transfert reçu depuis '+self.boxe_id_from.name,
            'user_id' : self.env.user.id,
            'boxe': self.boxe_id_to.id,
            'amount': self.amount,
            'mode': 'sold',
            'date_action': self.date_transfert,
            'date_valeur': self.date_transfert,
            'sens': 'credit',
        })
        envoi = obj.create({
            'operation': 'transfer',
            'name': 'Transfert envoye a '+self.boxe_id_to.name,
            'user_id' : self.env.user.id,
            'boxe': self.boxe_id_from.id,
            'amount': self.amount,
            'mode': 'sold',
            'date_action': self.date_transfert,
            'date_valeur': self.date_transfert,
            'sens': 'debit',
        })
        self.state = True
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
        }


