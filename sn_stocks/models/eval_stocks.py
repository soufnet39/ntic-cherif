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
    price_avg = fields.Float( string='Prix Achat Moyen',  readonly=True   )    
    montant = fields.Float( string='Montant',  readonly=True   )  
  
    @api.depends('stock_id')
    def _conv_str(self):
        for record in self:
            record.stock_id_str = str(record.stock_id.id) if record.stock_id else ''
        return True 

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
            select row_number() OVER () as id,
            t.company_id, p.id as product_id,avrprc.price_avg, p.name,t.stock_id, CAST(t.stock_id AS TEXT) stock_id_str,
 t.qty_calc , t.qty_calc*avrprc.price_avg as montant   
			from sn_sales_product as p 
            INNER JOIN 
            (select company_id,product_id,stock_id, sum(qty_stock) as qty_calc from sn_sales_commande_lines              
            group by product_id,company_id ,stock_id having sum(qty_stock)>0) as t 
            on p.id=t.product_id 
            INNER JOIN (
            select product_id,avg(price_unit) as price_avg from sn_sales_commande_lines  
            where operation_type='purchase'  group by product_id
            )as avrprc on p.id=avrprc.product_id 
            )''' % (self._table)
        )
