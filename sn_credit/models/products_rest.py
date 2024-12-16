from odoo import fields, models, tools
                 

class Credit_RestProduct(models.Model):
    _name = 'sn_credit.wiz_rest_product'
    _description = "product with stock"
    _auto = False

    # company_id = fields.Integer('company' )
    product_id = fields.Integer("Product ID")
    name = fields.Char("Nom")
    qty_calc = fields.Integer(string='Qte.')
    prices = fields.Char('Prix', help='List of all prices for this product')
    prix_mois = fields.Char('PrixMois', help='List of all prices for this product')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
            SELECT 
                pp.product_id as id, 
                pp.product_id, 
                pp.name, 
                t.qty_calc,
                string_agg(
                    CONCAT('[', CAST(pl."numberOfMonths" AS VARCHAR), '] ', to_char(p.fixed_price, 'FM999,999,999.00')),
                    ', ' ORDER BY p.fixed_price
                ) as prices,
				string_agg(
                    CONCAT('[', CAST(pl."numberOfMonths" AS VARCHAR), '] ', to_char(p.price_of_month, 'FM999,999,999.00')),
                    ', ' ORDER BY p.price_of_month
                ) as prix_mois
            FROM ( 
                SELECT ccp.id as product_id, ccp.name
                FROM sn_sales_product as ccp    
	          ) as pp 
            INNER JOIN (
                SELECT product_id, sum(qty_stock) as qty_calc 
                FROM sn_sales_commande_lines  
                GROUP BY product_id 
                HAVING sum(qty_stock) > 0
            ) as t ON pp.product_id = t.product_id
            LEFT JOIN sn_sales_pricelist_item p ON pp.product_id = p.product_id
            LEFT JOIN sn_sales_pricelist pl ON p.pricelist_id = pl.id
            GROUP BY pp.product_id, pp.name, t.qty_calc
            )""" % (self._table)
        )
