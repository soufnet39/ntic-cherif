from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from datetime import datetime


class wizInterStocks(models.TransientModel):
    _name = 'sn_stocks.interstocks'
    _description = 'transfert entre stocks'


    name = fields.Char('Name', default='Transfert entre stocks')
    note = fields.Char(string="Description", required=False)
    state = fields.Boolean(string="Status", default=False )
    date_transfert = fields.Date(string="Date de transfert", required=False,
                                 default=fields.Date.to_string(datetime.now()))

    stock_id_from = fields.Many2one(comodel_name="sn_stocks.stocks", string="Stock départ", required=True, )
    stock_id_to = fields.Many2one(comodel_name="sn_stocks.stocks", string="Stock destination", required=True, )
    interstock_lines = fields.One2many('sn_stocks.interstock_lines', 'operation_id', string='Lignes')
    stock_negatif = fields.Boolean(string="Stock exist",
            default=lambda self: self.env["ir.config_parameter"].sudo().get_param("sn_stocks.stock_negatif"))

    @api.constrains('stock_id_from', 'stock_id_to')
    def _constrain_2stocks(self):
        if self.stock_id_from == self.stock_id_to:
            raise ValidationError('Stock depart et Stock destination sont identiques')

    def do_transfert(self):
        if len(self.interstock_lines.read())==0:
            raise ValidationError('Aucun article a transferer!..')
        for t in self.interstock_lines:
            if t.qty<=0:
                raise ValidationError('Une des quantites est nulle!..')
        lines=[]
        if self.interstock_lines:
            lines_entree = [(0, 0, {    'product_id': line.product_id.id,
                                        'name': line.product_id.name ,
                                        'qty': line.qty,
                                        #'qty_done': line.qty,
                                        'price_unit': 122, #TODO to be corrected
                                        #'product_uom_qty_commanded':line.product_uom_qty,
                                        #'product_uom_qty_livred':line.product_uom_qty,
                                    }) for line in self.interstock_lines]

            lines_sortie = [(0, 0, {   'product_id': line.product_id.id,
                                        'name': line.product_id.name ,
                                        'qty': line.qty,
                                        #'qty_done': -1*line.qty,
                                        'price_unit': 122, #TODO to be corrected
                                        #'product_uom_qty_commanded':line.product_uom_qty,
                                        #'product_uom_qty_livred':line.product_uom_qty,
                                    }) for line in self.interstock_lines]
        obj = self.env['sn_sales.commandes']
        recu = obj.create({
            'name': '/',
            'reference': 'Transfert reçu depuis ' + self.stock_id_from.name,
            'document_type': 'entree',
            'remise_methode': 'taux',  # self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_methode', 'taux')
            'remise_applied_on' : 'global',   # self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_applied_on', 'global')
            'operation_type': '',
            'user_id': self.env.user.id,
            'stock_id': self.stock_id_to.id,
            'state': 'confirmed' if self.env['ir.config_parameter'].sudo().get_param('sn_stocks.operations_confirmed_by_default') else 'draft',
            'creation_date': fields.Date.today(), #self.date_transfert.strftime('%Y-%m-%d'),
            'confirmation_date': fields.Date.today() ,
            'note': self.note,
            'from_one_many_stock': 'one',
            'commande_lines':    lines_entree
        })
    #  'confirmation_date': self.date_transfert,
        envoi = obj.create({
            'name': '/',
            'reference': 'Transfert envoyé à ' + self.stock_id_to.name,
            'document_type': 'sortie',
            'operation_type': '',
            'remise_methode': 'taux',  # self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_methode', 'taux')
            'remise_applied_on' : 'global',   # self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_applied_on', 'global')
            'user_id': self.env.user.id,
            'stock_id': self.stock_id_from.id,
            'state': 'confirmed' if self.env['ir.config_parameter'].sudo().get_param('sn_stocks.operations_confirmed_by_default') else 'draft',
            'creation_date': fields.Date.today(), #self.date_transfert.strftime('%Y-%m-%d'),
            'confirmation_date': fields.Date.today() ,
            'note': self.note,
            'from_one_many_stock': 'one',
            'commande_lines': lines_sortie
        })


        self.state=True
        tree_view_id = self.env.ref('sn_stocks.sn_stocks_operations_tree').ids
        search_view_id = self.env.ref('sn_stocks.sn_stocks_operations_search_view').ids
        form_view_id = self.env.ref('sn_stocks.stocks_operation_form').ids
        # TODO:: search_view_id don't work properly
        return {
            'views': [[tree_view_id, 'tree'],   [search_view_id, 'search'],   [form_view_id, 'form']],
            'name': _('Mouvements des stocks'),
            'view_mode': 'tree,form',
            'res_model': 'sn_sales.commandes',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }


class wizInterStocksLine(models.TransientModel):
    _name = "sn_stocks.interstock_lines"
    _description = "Entre Stocks lines"

    sequence = fields.Integer(string='Sequence', default=10)
    stock_id_from = fields.Many2one('sn_stocks.stocks', related= 'operation_id.stock_id_from'  ,string='Depuis stock',  store=True )
    stock_negatif = fields.Boolean(string="Stock exist",related= 'operation_id.stock_negatif' )
    operation_id = fields.Many2one('sn_stocks.interstocks', string='Entre Stocks Opération Reference',
                                   required=True, ondelete='cascade',
                                   index=True, copy=False, readonly=True)

    product_id = fields.Many2one('sn_sales.product', string='Product', required=True, change_default=True,
                                 ondelete='restrict')

    qty = fields.Float(string='Qte.', required=True, digits="Quantity")
    qte_disponible = fields.Float(string='Quantite disponible',digits="Quantity",  ) #compute='_calcule_qte_disponible'

    # @api.onchange('product_id')
    # def _calcule_qte_disponible(self):
    #     for rec in self:
    #         if rec.product_id.id:
    #             qtys_in_same_stock = self.env['sn_sales.commande.lines'].search(
    #                     [('stock_id', '=', rec.stock_id_from.id),
    #                     ('product_id', '=', rec.product_id.id)])
    #             qtys = sum(r.qty_stock for r in qtys_in_same_stock)
    #             qqt = 0
    #             rec.qte_disponible=qtys
    #             if (isinstance(rec.id, int) or rec.id.ref != None): #and rec.product_id.id==self.product_id.id
    #                 qqt+=rec.qty
    #                 rec.qte_disponible=qtys+rec._origin.qty-qqt
