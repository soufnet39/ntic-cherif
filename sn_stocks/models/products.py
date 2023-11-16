from odoo import models, fields, api
from odoo.exceptions import UserError


class Stocks2Products(models.Model):
    _inherit = "sn_sales.product"

    stock_infini = fields.Boolean(string='Stock infini',help='Ne pas appliquer les règles de stocks' )


    def qte_product_function(self):
        tree_view_id = self.env.ref('sn_stocks.etatstocks_tree').ids
        search_view_id = self.env.ref('sn_stocks.sn_stock_operations_line_search_view').ids
        pivot_view_id = self.env.ref('sn_stocks.sn_stocks_operations_line_pivot').ids
        # TODO:: search_view_id don't work properly
        return {
            'views': [[tree_view_id, 'tree'], [search_view_id, 'search'], [pivot_view_id, 'pivot']],
            'name': self.name,
            'view_mode': 'tree',
            'res_model': 'sn_sales.commande.lines',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [("product_id", '=', self.id)]
        }
