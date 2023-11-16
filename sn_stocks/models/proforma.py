from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Ntic2Sales_SaleOrder(models.Model):

    _inherit = "sn_sales.proformas"


    @api.onchange('user_id' )
    def filtra_stock(self):
        res = {}
        if self.user_id.stock_ids:
            res['domain'] = {'stock_id': [ ('id', 'in', self.user_id.stock_ids.ids)]}
            adad = len(self.user_id.stock_ids)
            self.len_stock_id = adad
            if adad == 1:
                self.stock_id = self.user_id.stock_ids.ids[0]
        else:
            self.len_stock_id = 0
        return res

    stock_id = fields.Many2one('sn_stocks.stocks', )

    # stock_negatif = fields.Boolean(string="Stock exist", compute='_compute_stock_negatif',
    #                              default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
    #                                  'sn_stocks.stock_negatif'))
    from_one_many_stock = fields.Selection(string="", selection=[
        ('one', 'Depuis un seule stock'), ('many', 'Depuis plusieurs stocks'),
                ], default='one', required=False, store=False)
    len_stock_id = fields.Integer('Nombre de stocks',  )

    region = fields.Char(string="Region", related='stock_id.region_id.name', store=True)
    wilaya = fields.Char(string="Wilaya", related='stock_id.wilaya_id.name', store=True )

    # def _compute_stock_negatif(self):
    #     stock_negatif = self.env["ir.config_parameter"].sudo().get_param("sn_stocks.stock_negatif")
    #     for record in self:
    #         record.stock_negatif = stock_negatif

    @api.model
    def create(self, vals):
        seq = self.env['ir.config_parameter'].sudo().get_param('sn_sales.sequences')
        gwr = 'proforma'
        if seq == 'stock' or seq == 'wilaya' or seq == 'region':
            if not vals.get('stock_id'):
                raise UserError('Vous devez selectionner un stock!')
            if seq == 'stock':
                itscod = str(self.env['sn_stocks.stocks'].browse(vals.get('stock_id')).id)
            if seq == 'wilaya':
                itscod = self.env['sn_stocks.stocks'].browse(vals.get('stock_id')).wilaya_id.read()[0]['code']
            if seq == 'region' :
                itscod = self.env['sn_stocks.stocks'].browse(vals.get('stock_id')).region_id.read()[0]['code']
            gwr = seq + '_' + itscod
            next_one = self.env['ir.sequence'].get(gwr)
            if not next_one:
                dict = {"prefix": seq[0].upper() + itscod + '/',
                        "code": gwr,
                        "name": gwr + '_sequencer',
                        "active": True,
                        "padding": 4,
                        "implementation": "standard",
                        }
                self.env['ir.sequence'].create(dict)
                next_one = self.env['ir.sequence'].next_by_code(gwr)

            vals['name'] = next_one

        return super(Ntic2Sales_SaleOrder, self).create(vals)

class Ntic2Sales_SaleOrderLines(models.Model):
    _inherit = 'sn_sales.proforma.lines'

    stock_id = fields.Many2one('sn_stocks.stocks', related ='proforma_id.stock_id', string = 'Depuis stock', store=True  )
