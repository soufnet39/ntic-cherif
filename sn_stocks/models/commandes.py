from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

doc_types= {
        'livraison': 'BL',
        'reception': 'BR',
        'sortie':    'BS',
        'entree':    'BE',
}
senses = {'livraison': -1,
        'reception': 1,
        'sortie': -1,
        'entree': 1}

class Ntic2Commande_stock(models.Model):

    _inherit = "sn_sales.commandes"

    # extend original function in sn_sales
    def _default_confirmation_date(self):
        a = self._context.get("default_operation_type")=='command' and self.env['ir.config_parameter'].sudo().get_param('sn_sales.command_confirmed_by_default')
        b = self._context.get("default_operation_type")=='purchase' and self.env['ir.config_parameter'].sudo().get_param('sn_purchases.purchase_confirmed_by_default')

        c = self._context.get("default_document_type")=='livraison' and self.env['ir.config_parameter'].sudo().get_param('sn_stocks.delivery_confirmed_by_default')
        d = self._context.get("default_document_type")=='reception' and self.env['ir.config_parameter'].sudo().get_param('sn_stocks.reception_confirmed_by_default')
        e = (self._context.get("default_document_type")=='entree' or self._context.get("default_document_type")=='sortie') and self.env['ir.config_parameter'].sudo().get_param('sn_stocks.operations_confirmed_by_default')

        if a or b or c or d or e:
           return fields.Date.today()
    # extend original function in sn_sales
    def _default_state(self):
        a = self._context.get("default_operation_type")=='command' and self.env['ir.config_parameter'].sudo().get_param('sn_sales.command_confirmed_by_default')
        b = self._context.get("default_operation_type")=='purchase' and self.env['ir.config_parameter'].sudo().get_param('sn_purchases.purchase_confirmed_by_default')

        c = self._context.get("default_document_type")=='livraison' and self.env['ir.config_parameter'].sudo().get_param('sn_stocks.delivery_confirmed_by_default')
        d = self._context.get("default_document_type")=='reception' and self.env['ir.config_parameter'].sudo().get_param('sn_stocks.reception_confirmed_by_default')
        e = (self._context.get("default_document_type")=='entree' or self._context.get("default_document_type")=='sortie') and self.env['ir.config_parameter'].sudo().get_param('sn_stocks.operations_confirmed_by_default')

        if a or b or c or d or e:
           return 'confirmed'

        return 'draft'

    def _default_document_type(self):
        a = self._context.get("default_operation_type") == 'command' and self.env['ir.config_parameter'].sudo().get_param('sn_stocks.delivery_confirmed_by_default')
        b = self._context.get("default_operation_type") == 'purchase' and self.env['ir.config_parameter'].sudo().get_param('sn_purchases.purchase_confirmed_by_default')
        if a:
            return 'livraison'
        if b:
            return 'reception'
        return ''

    @api.depends('user_id')
    def _calcule_nbr_stocks(self):
        for rec in self:
            rec.len_stock_id=len(rec.user_id.stock_ids)

    @api.onchange('user_id')    #, 'from_one_many_stock'
    def filtra_stocks(self):
        res = {}
        self.stock_id=0
        if self.user_id.stock_ids:
            res['domain'] = {'stock_id': [('id', 'in', self.user_id.stock_ids.ids)]}
            if len(self.user_id.stock_ids)==1:
                self.stock_id=self.user_id.stock_ids[0].id
            else:
                return res


    reference = fields.Char(string='Référence',)
    operation = fields.Char(string='Opération', default='/')
    state = fields.Selection(default=_default_state)  # inherited form sn_sales
    confirmation_date = fields.Date( default=_default_confirmation_date) # inherited form sn_sales
    stock_negatif = fields.Boolean(string="Stock exist",compute="_stk_neg" )

    stock_id = fields.Many2one('sn_stocks.stocks')

    len_stock_id = fields.Integer('Nombre de stocks',
            compute='_calcule_nbr_stocks',
            default=lambda self: len(self.user_id.stock_ids))

    delivery_confirmed = fields.Boolean(string="Livraison confirmé",
            default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_stocks.delivery_confirmed_by_default'),
            compute='_compute_delivery'
            )
    # qty_delivered_equals_commanded = fields.Boolean("Qte Cmd = Qte Liv",
    #         default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_stocks.qty_delivered_equals_commanded'))


    document_type = fields.Selection([
        ('livraison', 'Bon de livraison'),
        ('reception', 'Bon de recéption'),
        ('sortie', 'Bon de sortie'),
        ('entree', 'Bon d\'entrée'),
    ],
        string='Type de document', copy=False, default=_default_document_type  ) # default='livraison' if delivery comfirmed by default

    from_one_many_stock = fields.Selection(string="Source", selection=[
        ('one', 'Mono stock'), ('many', 'Multi stocks'),
    ], default='one', required=True, store=True)
    region = fields.Char(string="Region", related='stock_id.region_id.name', store=True)
    wilaya = fields.Char(string="Wilaya", related='stock_id.wilaya_id.name', store=True)


    @api.depends('operation')
    def _stk_neg(self):
        self.stock_negatif=self.env["ir.config_parameter"].sudo().get_param("sn_stocks.stock_negatif")

    @api.depends('name', 'operation', 'operation_type')
    def name_get(self):
        result = []
        for rec in self:
            if rec.operation_type in ['purchase','command']:
                result.append((rec.id, rec.name))
            else:
                result.append((rec.id, rec.operation))
        return result

    @api.model
    def _compute_delivery(self):
        for record in self:
            record.delivery_confirmed = self.env['ir.config_parameter'].sudo().get_param('sn_stocks.delivery_confirmed_by_default')

    def print_operation_stock(self):
        return self.env.ref('sn_stocks.action_report_op_stock').report_action(self)

    def go2piece(self):
        piece = self.env.context.get('piece')
        form=''
        if piece == "livraison":
            title = 'Bon de livraison'
            form  = 'sn_stocks.stocks_operation_form'
        if piece == "reception":
            title = 'Bon de recéption'
            form  = 'sn_stocks.stocks_operation_form'
        if piece == "commande":
            title = 'Bon de Commande'
            form  = 'sn_stocks.view_order_form_inherited1'
        if piece == "purchase":
            title = "Bon d'Achat"
            form  = 'sn_purchases.purchases_form'

        if form == '':
            return {}

        form_view_id = self.env.ref(form).ids
        return {
                'views': [[form_view_id, 'form']],
                'name': _(title),
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': form_view_id,
                'res_model': 'sn_sales.commandes',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.id
        }

    @api.model
    def create(self, vals):
        dt=''
        if vals.get('document_type'):
            dt= doc_types[vals['document_type']]

            seq = self.env['ir.config_parameter'].with_user(True).get_param('sn_sales.sequences') or 'global'
            if seq == 'stock' or seq == 'wilaya' or seq == 'region':
                if not vals.get('stock_id'):
                    raise UserError('Vous devez selectionner un stock!')
                if seq == 'stock':
                    itscod = str(self.env['sn_stocks.stocks'].browse(vals.get('stock_id')).id)
                if seq == 'wilaya':
                    itscod = self.env['sn_stocks.stocks'].browse(vals.get('stock_id')).wilaya_id.read()[0]['code']
                if seq == 'region':
                    itscod = self.env['sn_stocks.stocks'].browse(vals.get('stock_id')).region_id.read()[0]['code']
                gwr = dt+ '_' +seq + '_' + itscod
                next_one = self.env['ir.sequence'].get(gwr)
                if not next_one:
                    dict = {"prefix": dt+seq[0].upper() + itscod + '/',
                            "code": gwr,
                            "name": gwr + '_sequencer',
                            "active": True,
                            "padding": 4,
                            "implementation": "standard",
                            }
                    self.env['ir.sequence'].create(dict)
                    next_one = self.env['ir.sequence'].next_by_code(gwr)
            else:
                gwr = vals['document_type']
                next_one = self.env['ir.sequence'].get(gwr)
                if not next_one:
                    dict = {"prefix": dt + '/',
                            "code": gwr,
                            "name": gwr + '_sequencer',
                            "active": True,
                            "padding": 4,
                            "implementation": "standard",
                            }
                    self.env['ir.sequence'].create(dict)
                    next_one = self.env['ir.sequence'].next_by_code(gwr)

            vals['operation'] = next_one

        return super(Ntic2Commande_stock, self).create(vals)


class Ntic2CommandeLines_Stock(models.Model):
    _inherit = 'sn_sales.commande.lines'

    stock_id = fields.Many2one('sn_stocks.stocks', related= 'commande_id.stock_id'  ,string='Depuis stock',  store=True )
    stock_negatif = fields.Boolean(string="Stock exist",related='commande_id.stock_negatif' )
    # TODO:: qty_done DEPRICATED
    qty_done= fields.Float(string='Qte.', digits="Quantity" ) #, compute='_qty_done', store=True
    qty_stock= fields.Float(string='Qte.', digits="Quantity" , compute='_calculate_qty_stock', store=True) 
    qte_disponible = fields.Float(string='Quantite disponible', digits="Quantity",readonly=True) #compute='_calculate_qty_disponible'
    stock_infini = fields.Boolean(string='Stock infini',related="product_id.stock_infini" , store=True )
    # qte modified on source : =1 -> if stock can be negatif, =0 -> if stock cannot be negatif
    #qty = fields.Float(string='Qte.', digits="Quantity", default=lambda self: 1.0 if self.env["ir.config_parameter"].sudo().get_param("sn_stocks.stock_negatif") else 0.0 )
    
     

    @api.depends('qty')
    def _calculate_qty_stock(self):
            for rec in self:  
                  dt=rec.commande_id.document_type
                  if (dt):
                     rec.qty_stock = senses[dt]*rec.qty
                  else:
                      rec.qty_stock=0               
           
 
   

    @api.onchange('product_id','qty')
    def _calcule_qte_disponible(self):
          for rec in self:   
            if (rec.commande_id.document_type in ["reception","entree"]):
                return
            if rec.product_id.id:
                qtys_in_same_stock = self.env['sn_sales.commande.lines'].search(
                        [('stock_id', '=', rec.stock_id.id),
                        ('product_id', '=', rec.product_id.id)])
                qtys =  sum(r.qty_stock for r in qtys_in_same_stock)
                rec.qte_disponible=qtys+rec._origin.qty
                if(rec.product_id.stock_infini):
                    rec.qty=1
                else:
                    rec.qty= max(rec.qte_disponible,0) if rec.qty>rec.qte_disponible else rec.qty
                #qqt = 0
                #for c in self.commande_id.commande_lines:
                # if (isinstance(rec.id, int) or rec.id.ref != None): #and rec.product_id.id==self.product_id.id
                #     qqt+=rec.qty_stock
                #     rec.qte_disponible=qtys+rec._origin.qty+qqt
            
            
