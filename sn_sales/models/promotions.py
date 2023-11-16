from odoo import api, models, fields
#from odoo.exceptions import UserError, ValidationError

class SnStocksReserves(models.Model):
    _name = "sn_sales.promotions"
    _description = "Gestion des promotins accasionels"


    name = fields.Char(string="Titre", required=True, )


    # product_category = fields.Many2many(comodel_name='sn_sales.productcategory',  string="Catégories de Produits",)
    products_ids = fields.Many2many(comodel_name='sn_sales.product',  string="Produits en question",  )
    #products_ids_concerned
    active = fields.Boolean('Active', default=True, help="Si non, Cette promotion sera cache et non supprime.")

    promotion_type = fields.Selection(string="Type de promotion",
                                      selection=[('amount', 'Montant'),
                                                 ('percent', 'Pourcentage'), ], required=True, default='percent' )


    clients_category = fields.Many2many(comodel_name='sn_sales.partner',  string="Type de clients",)
    clients_ids = fields.Many2many(comodel_name='sn_sales.partner',  string="Type de clients",)
    # client_ids_concerned

    date_start = fields.Date(string="Date debut",  )
    date_end = fields.Date(string="Date fin",  )
    # TODO :: date_start <= date_end
