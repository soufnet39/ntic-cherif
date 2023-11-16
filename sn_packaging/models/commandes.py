from odoo import models, fields, tools

class SnUomCommandes(models.Model):
    _inherit = "sn_sales.commandes"

    using_logistics = fields.Boolean(string="Utiliser les logistiques",  default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.using_logistics'))
    total_weight = fields.Float("Poids Total", readonly=True, compute="_compute_logistics")
    total_volume = fields.Float("Volume Total", readonly=True, compute="_compute_logistics")


    @api.depends('commande_lines.qty')
    def _compute_logistics(self):
        for rec in self:
            cl = rec.commande_lines
            totP=0
            totV=0
            for r in cl:
                totP+=r.qty*r.product_id.weight
                totV+=r.qty*r.product_id.volume
            rec.update({
                'total_weight': totP,
                'total_volume': totV
            })




    # @api.onchange('using_logistics')
    # def _using_logistics_changed(self):
    #     for l in self.commande_lines:
    #         #l.product_colisage= False
    #         l.qty=1
        #self._compute_logistics()
