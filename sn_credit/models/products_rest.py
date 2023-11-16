from odoo import api, fields, models, tools
                 

class Credit_RestProduct(models.Model):
    _name = 'sn_credit.wiz_rest_product'
    _description = "product with stock"
    _auto = False

    company_id = fields.Integer('company' )
    product_id = fields.Integer("Product ID")
    name = fields.Char("Nom")
    qty_calc = fields.Integer(string='Qte.')
    price = fields.Float('Prix')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
            select row_number() OVER () as id, pp.product_id, pp.name, t.qty_calc,pp.price 
          from ( 
          select ccp.id as product_id,ccp.name, CASE WHEN ccp.default_price IS NULL THEN 0 ELSE ccp.default_price END as price
            from sn_sales_product as ccp            
          ) as pp 
            INNER JOIN 
            (select product_id, sum(qty_stock) as qty_calc from sn_sales_commande_lines  
            group by product_id having sum(qty_stock)>0 ) as t on pp.product_id=t.product_id
            )''' % (self._table)
        )
