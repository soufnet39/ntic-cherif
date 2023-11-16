from odoo import api, models, fields, _

class BoxesModule(models.Model):
    _name = 'sn_boxes.boxes'
    _description = 'Ntic Comptes of money'

    def _get_types(self):
        # ('initial',  'Solde Initial'),
        vals=[  ('bank',  'Banque'),  ('sold',  'Espèce'),  ('other',  'Autres') ]
        # if self.env['ir.module.module'].search_count([('name', '=', 'sn_employees'), ('state', '=', 'installed')])==1:
        #     vals.extend([('person', 'Lié a une personne ')])
        # if self.env['ir.module.module'].search_count([('name', '=', 'sn_stocks'), ('state', '=', 'installed')])==1 :
        #     vals.extend([('stock', 'Lié a un stock ')])
        return vals

    name = fields.Char(string="Compte",  required=True, translate=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sn_boxes.boxes'))

    boxe_type = fields.Selection(string="Type", selection=_get_types, required=True)
    
    other=  fields.Char(  string='Autre',  )
    

    # person_id = fields.Many2one(comodel_name="sn_employees.employees", string="Personne", required=False, )
    # le stock_id active' fait error
    # stockid = fields.Many2many(comodel_name='sn_stocks.stocks',  string="Stock", )

    user_ids = fields.Many2many(comodel_name="res.users", string="Responsables", )

    rib = fields.Char(string="RIB", required=False, )
    bank = fields.Char(string="Banque", required=False, )
    agence = fields.Char(string="Agence", required=False, )

    wilaya_id = fields.Many2one("sn_base.wilayates", string='Wilaya', required=True)

    region = fields.Many2one( related='wilaya_id.region_id', store=True)

    boxe_operations= fields.One2many('sn_boxes.operations','boxe')

    sold_boxe = fields.Float(string='Sold Compte', compute='_calcule_sold_boxe', store=True  )

    _sql_constraints = [
        ('boxes_distinct',
         'unique(name)',
         'Les noms des comptes doivent être uniques.'),
    ]

    @api.depends('boxe_operations.amount_done')
    def _calcule_sold_boxe(self):
        for rec in self:
            vl = 0
            for vi in rec.boxe_operations:
                vl+=vi['amount_done']
            rec.update({'sold_boxe': vl})

    # the bellow functin duplicated a in sn_boxes.operations

    def sold_boxe_function(self):
        tree_view_id = self.env.ref('sn_boxes.sn_boxes_operations_list_view').ids
        search_view_id = self.env.ref('sn_boxes.sn_boxes_operations_search_view').ids
        form_view_id = self.env.ref('sn_boxes.sn_boxes_operations_form_view').ids
        #TODO:: search_view_id don't work properly
        return {
            'views': [[tree_view_id, 'tree'],[form_view_id, 'form'],[search_view_id, 'search']],
            'name': _('Opérations'),
            'view_mode': 'tree',
            'res_model': 'sn_boxes.operations',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [("boxe", '=', self.id)]
        }


