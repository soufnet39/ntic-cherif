from odoo import api, models, fields, tools

class NticAksatsMonthsLines(models.Model):
    _name = "sn_stocks.eval_stocks"
    _description = "Evaluation de stocks"
    _auto = False

    company_id = fields.Many2one('res.company', 'Company',readonly=True )
    product_id = fields.Integer( string='Id',  readonly=True   )
    name = fields.Char( string='Produit',  readonly=True   )   
    stock_id = fields.Many2one('sn_stocks.stocks', 'stock',readonly=True ) 
    stock_id_str = fields.Char(   readonly=True  )    
    
    qty_calc = fields.Float( string='Qte.',  readonly=True, digits="Quantity"   )    
    avg_price = fields.Float( string='Moy.Prix',  readonly=True   )  
    last_price = fields.Float( string='Der.Prix',  readonly=True   )  
    avg_montant = fields.Float( string='Moy.Mta.',  readonly=True   )  
    last_montant = fields.Float( string='Der.Mta.',  readonly=True   )  
  
    @api.depends('stock_id')
    def _conv_str(self):
        for record in self:
            record.stock_id_str = str(record.stock_id.id) if record.stock_id else ''
        return True 

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
            SELECT  row_number() OVER () as id,
                    t.company_id,
                    p.id AS product_id,  
                    p.name,
                    t.stock_id,
                    CAST(t.stock_id AS TEXT) AS stock_id_str,
                    t.qty_calc,
                    prx.avg_price,
                    prx.last_price,
                    t.qty_calc * prx.avg_price AS avg_montant,
                    t.qty_calc * prx.last_price AS last_montant
                FROM 
                    sn_sales_product AS p
                 INNER JOIN 
                    (select company_id,product_id,stock_id, sum(qty_stock) as qty_calc from sn_sales_commande_lines              
                    group by product_id,company_id ,stock_id having sum(qty_stock)>0) as t 
                    on p.id=t.product_id 
                INNER JOIN (
                    select aa.product_id, aa.price_unit as last_price,bb.avg_price
                From
                (SELECT product_id, price_unit
                FROM (
                    SELECT 
                        product_id,
                        write_date,
                        price_unit,
                        ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY write_date DESC) AS rn
                    FROM sn_sales_commande_lines
                    WHERE operation_type = 'purchase' 
                ) AS ranked
                WHERE rn = 1) as aa
                inner join (
                    SELECT 
                        product_id,
                        AVG(price_unit) as avg_price       
                    FROM 
                        sn_sales_commande_lines 
                    where  operation_type = 'purchase' 
                    group by product_id
                ) as bb
                on aa.product_id=bb.product_id
                    
                ) AS prx
                    ON p.id = prx.product_id
            )''' % (self._table)
        )
