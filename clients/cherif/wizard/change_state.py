from odoo import models, fields, api


class ChangeOrderStateWizard(models.TransientModel):
    _name = 'cherif.commandes_states_wizard'

    new_state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('canceled', 'Annulée')        
    ], string='Convert to this New State', default='draft', required=True, help='This will change the state of the selected records')

    # @api.multi
    def change_state(self):
        orders_to_update = self.env['sn_sales.commandes'].browse(self.env.context.get('active_ids'))
        orders_to_update.write({'state': self.new_state})  # Replace 'state_field_name' with the actual field name representing the state in your model
        return {'type': 'ir.actions.act_window_close'}
