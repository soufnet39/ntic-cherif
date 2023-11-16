from odoo import models, fields, api


class StocksSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    stock_negatif = fields.Boolean(string="Vendre meme stocks négatifs", config_parameter='sn_stocks.stock_negatif')
    operations_confirmed_by_default = fields.Boolean( string="Tous les opérations entree/sortie stocks sont confirmées par défaut",config_parameter='sn_stocks.operations_confirmed_by_default')
    delivery_confirmed_by_default = fields.Boolean(  "La livraison automatique à la commande",config_parameter='sn_stocks.delivery_confirmed_by_default')
    reception_confirmed_by_default = fields.Boolean(  "La Réception automatique à l'achat", config_parameter='sn_stocks.reception_confirmed_by_default')
    purchase_to_stocks = fields.Selection(string="Acheter et déposer sur multi Stocks?",
            selection=[('mono', 'One Stock only'), ('multi', 'Many stocks')],
            default='mono',
            required=True,
            config_parameter='sn_stocks.purchase_to_stocks')
    sale_from_stocks = fields.Selection(string="Vendre depuis multi stocks?",
            selection=[('mono', 'One Stock only'), ('multi', 'Many stocks')],
            required=True,
            default='mono',
            config_parameter='sn_stocks.sale_from_stocks')
    #default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_stocks.sale_from_stocks' )
    # qty_delivered_equals_commanded = fields.Boolean("toujours Qte livrée = commandée?", config_parameter='sn_stocks.qty_delivered_equals_commanded')
    sequences = fields.Selection(string="Numérotation, bons de Vente",
                                 selection=[
                                     ('global', 'Numérotation globale'),
                                     ('stock',  'Numérotation par stock'),
                                     ('region', 'Numérotation par region (stock)'),
                                     ('wilaya', 'Numérotation par wilaya (stock)')
                                 ], default='global'
                                 )
