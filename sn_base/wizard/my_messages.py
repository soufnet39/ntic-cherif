from odoo import api, fields, models, _

class sn_base_message_wizard(models.TransientModel):
    _name = "sn_base.message_wizard"
    _description = "Message wizard to display warnings, alert ,success messages"

    def get_default(self):
        if self.env.context.get("message", False):
            return self.env.context.get("message")
        return False

    name = fields.Text(string="Message", readonly=True, default=get_default)

    @api.model
    def message(self, title='Message', message='' ):

        form_view_id = self.env.ref('sn_base.my_message_wizard').ids
        context = dict(self._context or {})
        context['message'] = message
        return {
            'views': [[form_view_id, 'form']],
            'name': title,
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': form_view_id,
            'res_model': 'sn_base.message_wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }


