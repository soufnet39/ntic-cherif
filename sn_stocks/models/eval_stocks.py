from odoo import models, fields, tools

class NticAksatsMonthsLines(models.Model):
    _name = "sn_stocks.eval_stocks"
    _description = "Evaluation de stocks"
    _auto = False

    product_id = fields.Integer( string='Id',  readonly=True   )
    company_id = fields.Many2one('res.company', 'Company',readonly=True )
    name = fields.Char( string='Produit',  readonly=True   )    
    qty_calc = fields.Float( string='Qte.',  readonly=True, digits="Quantity"   )    
    price_avg = fields.Float( string='Prix Achat Moyen',  readonly=True   )    
    montant = fields.Float( string='Montant',  readonly=True   )  
  
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
            select row_number() OVER () as id,
            t.company_id, p.id as product_id,avrprc.price_avg, p.name, t.qty_calc , t.qty_calc*avrprc.price_avg as montant   
			from sn_sales_product as p 
            INNER JOIN 
            (select company_id,product_id, sum(qty_stock) as qty_calc from sn_sales_commande_lines              
             group by product_id,company_id having sum(qty_stock)>0) as t 
            on p.id=t.product_id 
            INNER JOIN (
            select product_id,avg(price_unit) as price_avg from sn_sales_commande_lines  
            where operation_type='purchase'  group by product_id
            )as avrprc on p.id=avrprc.product_id 
            )''' % (self._table)
        )

        #   where company_id in %s
        #   '(' + ', '.join('{}'.format(t) for t in self.env.user.company_ids.ids) + ')'