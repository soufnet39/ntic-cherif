import datetime
from odoo import fields, models
from odoo.exceptions import UserError,ValidationError


class CherifRestProductCtrl(models.TransientModel):
    _name = 'cherif.product_rest_ctrl'
    _description = "product rest control"

    def _default_year(self):
        now = datetime.datetime.now()
        return str(now.year)
    
    def _default_month(self):
        now = datetime.datetime.now()
        return str(now.month)
    
    name = fields.Char('Name', default='default')
    mois = fields.Selection(
        string='Mois',
        selection=[
            ('1', 'Janvier'),
            ('2', 'Février'),
            ('3', 'Mars'),
            ('4', 'Avril'),
            ('5', 'Mai'),
            ('6', 'Juin'),
            ('7', 'Juillet'),
            ('8', 'Août'),
            ('9', 'Septembre'),
            ('10', 'Octobre'),
            ('11', 'Novembre'),
            ('12', 'Décembre')],
             default=_default_month,
             required=True
        )
    annee = fields.Selection(
        string='Année',
        selection=[('2023', 2023),('2024', 2024),('2025', 2025),('2026', 2026)],
        default=_default_year,
        required=True
        )
    lines_ids = fields.One2many('cherif.product_rest_ctrl_detail',"rest_ctrl_id", string='details' )

    def faltara(self):
            self.lines_ids = [(5,0,0)]        
            self.env.cr.execute('''            
                    SELECT pp.product_id AS id, pp.name, t.qty
                    FROM (
                        SELECT ccp.id AS product_id, ccp.name,
                            CASE WHEN ccp.default_price IS NULL THEN 0 ELSE ccp.default_price END AS price
                        FROM sn_sales_product AS ccp
                    ) AS pp
                    INNER JOIN (
                        SELECT scl.product_id, SUM(scl.qty_stock) AS qty
                        FROM sn_sales_commande_lines AS scl
                        INNER JOIN sn_sales_commandes AS sc ON scl.commande_id = sc.id
                        WHERE sc.confirmation_date < DATE_TRUNC('month', MAKE_DATE(%s, %s, 1))
                        GROUP BY scl.product_id
                        HAVING SUM(scl.qty_stock) > 0
                    ) AS t ON pp.product_id = t.product_id
                    ''' % (self.annee,self.mois)
                )
            lines = self.env.cr.fetchall()
            tmp_lines = []
            if lines:
                for rtd in lines: 
                    tmp_lines.append((0, 0, {
                                'product_id' : rtd[0], 
                                'name' : rtd[1], 
                                'qty' : rtd[2], 
                            }))
            else:
                raise ValidationError(_('Pas de stock'))

            self.lines_ids = tmp_lines

    def print_etat_stock_ctrl(self):
        return self.env.ref('cherif.cherif_etatstock_ctrl').report_action(self)
         

class CherifRestProductCtrlDetail(models.TransientModel):
    _name = 'cherif.product_rest_ctrl_detail'
    _description = "product rest control detail"

    rest_ctrl_id = fields.Many2one('cherif.product_rest_ctrl', string='reste Reference',
                               required=True, ondelete='cascade',
                               index=True,copy=False)
    
    product_id = fields.Integer("Product ID")
    name = fields.Char("Nom")
    qty = fields.Integer(string='Qte.')

   
