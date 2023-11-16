from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

class SnStocksReserves(models.Model):
    _name = "sn_stocks.reserves"
    _description = "Gestion des quotas de reserve par stock"


    name = fields.Char(string="Titre", required=True, )

    # product_category = fields.Many2many(comodel_name='sn_sales.productcategory', string="Catégories de Produits", )
    products_ids = fields.Many2many(comodel_name='sn_sales.product', string="Produits en question", )

    stock_ids = fields.Many2many(comodel_name="sn_stocks.stocks",  string="Stocks en question", )
    active = fields.Boolean('Active', default=True, help="Si non, Ce reserve sera cache et non supprime.")

    reserve_qte = fields.Float(string="Quantite en reserve", default=0.0   )

    date_start = fields.Date(string="Date debut",  )
    date_end = fields.Date(string="Date fin",  )
    # TODO :: date_start <= date_end
    # TODO:: Ajouter des conditions sur la montant total (si > a un certain valeur pour appliquer la promotions)


