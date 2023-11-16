from odoo import api, models, fields, _

class NticBoxesPartner(models.Model):
    _inherit = 'sn_sales.partner'

    client_operations = fields.One2many('sn_boxes.operations', 'partner_id')

    sold_client = fields.Float(string='Sold Client', compute='_calcule_sold_client', store=True )


    @api.depends('client_operations.amount_done')
    def _calcule_sold_client(self):
        for rec in self:
            vl = 0
            for vi in rec.client_operations:
                vl+=vi['amount_done']
            rec.update({'sold_client': vl})

    # the bellow functin duplicated a in sn_boxes.operations

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
            'domain': [("partner_id", '=', self.id)]
        }