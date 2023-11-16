from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

class SnStocksStocks(models.Model):
    _name = "sn_stocks.stocks"
    _description = "Ntic Stocks"
    _order = 'name'


    name = fields.Char('Name', index=True, required=True, translate=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sn_stocks.stocks'))

    can_be_negatif = fields.Boolean(string="Stock negatif", default=False  )
    # ('arrival', 'Arrivage (Achat)'), with purchase module
    nature = fields.Selection(string="Nature",
                              selection=[
                                         ('fix', 'Fixe'),
                                         ('mobil', 'Mobile'),
                                         ('virtual', 'Virtuel'),
                                         ], required=True, default='fix')


    user_ids = fields.Many2many( "res.users", string= "Responsables", )

    wilaya_id = fields.Many2one("sn_base.wilayates", string='Wilaya', required=True )
    region_id = fields.Many2one("sn_base.regions", related='wilaya_id.region_id' ,store=True)
    commune_id = fields.Many2one("sn_base.communes", string='Commune', )
    description=fields.Char(string='Description')
    # product_count = fields.Integer(
    #     '# Products', compute='_compute_product_count',
    #     help="The number of products under this stock (Does not consider the children categories)")

    def stock_function(self):
        tree_view_id = self.env.ref('sn_stocks.sn_stocks_operations_tree').ids
        search_view_id = self.env.ref('sn_stocks.sn_stocks_operations_search_view').ids
        form_view_id = self.env.ref('sn_stocks.stocks_operation_form').ids
        # TODO:: search_view_id don't work properly
        return {
            'views': [[tree_view_id, 'tree'], [form_view_id, 'form'], [search_view_id, 'search']],
            'name': self.name,
            'view_mode': 'tree',
            'res_model': 'sn_sales.commandes',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [("stock_id", '=', self.id)]
        }

    # @api.depends('wilaya_id')
    # def get_region(self):
    #     self.region_id = self.wilaya_id.region_id

    @api.onchange('wilaya_id')
    def _get_communes(self):
        res = {}
        res['domain'] = {'commune_id': [('wilaya_id', '=', self.wilaya_id.id)]}
        self.commune_id = ''
        return res


    def _compute_product_count(self):
        read_group_res = self.env['product.template'].read_group([('categ_id', 'child_of', self.ids)], ['categ_id'], ['categ_id'])
        group_data = dict((data['categ_id'][0], data['categ_id_count']) for data in read_group_res)
        for categ in self:
            product_count = 0
            for sub_categ_id in categ.search([('id', 'child_of', categ.id)]).ids:
                product_count += group_data.get(sub_categ_id, 0)
            categ.product_count = product_count


    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    # TODO: _sql_constraints (name unique)

