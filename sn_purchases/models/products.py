from odoo import models, fields, tools,api, _
from odoo.exceptions import ValidationError, RedirectWarning, UserError

class NticAchatProduct(models.Model):
    _inherit = "sn_sales.product"

    # def _get_default_uom_id(self):
    #     return super(NticAchatProduct, self)

    purchase_ok = fields.Boolean('Peut être acheté', default=True)
    purchase_price = fields.Float('Prix d\'achat',
                                  digits='Product Price',
                                  groups="base.group_user", )
    pmp_price = fields.Float('Prix moyen pondere (PMP)',
                             digits='Product Price',
                             groups="base.group_user",)

   # uom_purchase_id = fields.Many2one('sn_sales.uom', 'Unité de Mesure Achat', help="Unité de mesure d'achat par defaut.") # default=_get_default_uom_id,
    code_supplier = fields.Char('Reference fournisseur', )
    sale_base_on = fields.Selection(string="Prix de vente basé sur",
                                    selection=[('achat', 'Prix d\'achat'), ('pmp', 'PMP'), ], default='achat', )
    sale_percentage = fields.Float(string="Taux de Calcule", required=False  )

    # @api.onchange('uom_sale_id','uom_purchase_id' )
    # def _onchange_uom(self):
    #     if self.uom_sale_id and self.uom_purchase_id and self.uom_sale_id.category_id != self.uom_purchase_id.category_id:
    #         raise ValidationError(
    #             _('Les unites de mesure du vente et achat doivent être de même famille.'))
    #         self.uom_purchase_id = self.uom_sale_id

    # @api.onchange('sale_percentage','purchase_price' )
    # def _onchange_sale_percentage(self):
    #     if self.sale_base_on == 'achat' and self.sale_percentage!=0.0:
    #         self.default_price = self.purchase_price * self.sale_percentage

