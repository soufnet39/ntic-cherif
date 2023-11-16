from odoo import models, fields, api, _

class NticSaleCommande(models.Model):
    _inherit = "sn_sales.commandes"

    facture_image = fields.Integer(string='Facture en relation',copy=False, default=0 )
    facture_name = fields.Char(string='Facture',copy=False, default='' )
    extra_id = fields.Many2one('sn_invoices.invoices')

    def go2facture(self):
        fctr_ref = self.env['sn_invoices.invoices'].search_count([('id', '=', self.facture_image)])
        if fctr_ref > 0:
            form_view_id = self.env.ref('sn_invoices.view_facture_form').ids
            return {
                'views': [[form_view_id, 'form']],
                'name': _('Facture'),
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': form_view_id,
                'res_model': 'sn_invoices.invoices',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.facture_image
            }
        else:
            self.facture_image=0
            self.facture_name=''
            message = _('Facture en relation non trouvée!.. Peut être supprimée.. Cette relation sera désormais déconnectée')
            title= _('Problème de liaison entre pièces')

            return self.env['sn_base.message_wizard'].message(title, message)

    def action_convert2facture(self):
        filb_values = [(0, 0, {'name': line.name,                               
                               'product_id': line.product_id.id,
                               'sequence': line.sequence,
                               'price_unit': line.price_unit,
                               'price_total': line.price_total,
                               'remise_taux': line.remise_taux,
                               'remise_mta': line.remise_mta,
                               'product_code': line.product_code,
                               'qty': line.qty,                               
                               'product_image': line.product_image,
                               'display_type': line.display_type,
                               }) for line in self.commande_lines]

        ctx = {
            'default_commande_origin': self.id,  # may be groupe od cmds to 1 facture
            'default_partner_id': self.partner_id.id,
            'default_creation_date': fields.Date.today(),
            'default_user_id': self.user_id.id,
            'default_tva_exist': self.tva_exist,
            'default_tva_taux': self.tva_taux,
            'default_remise_exist': self.remise_exist,
            'default_remise_taux': self.remise_taux,
            'default_remise_mta': self.remise_mta,
            'default_remise_methode': self.remise_methode,
            'default_remise_applied_on': self.remise_applied_on,
            'default_remise_valeur': self.remise_valeur,

            'default_company_id': self.company_id.id,
            'default_product_name_editable': self.product_name_editable,

            'default_facture_lines': filb_values,
            'default_code_article_exist': self.code_article_exist,
        }

        form_view_id = self.env.ref('sn_invoices.view_facture_form').ids
        return {
            'views': [[form_view_id, 'form']],
            'name': _('Facture'),
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': form_view_id,
            'res_model': 'sn_invoices.invoices',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': ctx,
        }
