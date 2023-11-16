from odoo import models, fields, api, _
from odoo.osv.expression import get_unaccent_wrapper

class NticInvoicesPartner(models.Model):
    _inherit = 'sn_sales.partner'
    _description = "Facturation of partner"

    def client_factures(self):
        tree_view_id = self.env.ref('sn_invoices.view_invoices_tree').ids
        return {
                'views': [[tree_view_id, 'tree']],
                'name': _('Factures Client'),
                'view_mode': 'form',
                'view_id': tree_view_id,
                'res_model': 'sn_invoices.invoices',
                'type': 'ir.actions.act_window',
                'domain': [("partner_id", '=', self.id)],
                'target': 'current',
             
            }
