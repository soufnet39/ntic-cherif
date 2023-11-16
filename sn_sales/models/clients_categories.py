from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
#
#
#  GOOD EXAMPLE OF PARENT CHILD RELATION
#
#
class SnClientsCategories(models.Model):

    _name = "sn_sales.clients_categories"
    _description = "Ntic Clients Catégories"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('Name', index=True, required=True, translate=True)
    complete_name = fields.Char( 'Nom Complèt', compute='_compute_complete_name',    store=True)
    parent_id = fields.Many2one('sn_sales.clients_categories', 'Parent', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many('sn_sales.clients_categories', 'parent_id', 'Child Catégories')
    client_count = fields.Integer(
        'Nombre de clients', compute='_compute_client_count',
        help="Le nombre de clients sous cette categorie (y compris les sous catégories )")

    _sql_constraints = [
        ('ntic_client_category_name_unique',
         'UNIQUE (complete_name)',
         'Le nom de Category doit être unique.'),
    ]

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for cat in self:
            if cat.parent_id:
                cat.complete_name = '%s / %s' % (cat.parent_id.complete_name, cat.name)
            else:
                cat.complete_name = cat.name

    def _compute_client_count(self):
        read_group_res = self.env['sn_sales.partner'].read_group([('tasnif', 'child_of', self.ids)], ['tasnif'],
                                                                 ['tasnif'])
        group_data = dict((data['tasnif'][0], data['tasnif_count']) for data in read_group_res)
        for categ in self:
            client_count = 0
            for sub_tasnif in categ.search([('id', 'child_of', categ.id)]).ids:
                client_count += group_data.get(sub_tasnif, 0)
            categ.client_count = client_count

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Vous ne pouvez pas créer de relation de catégorie récursive.'))
        return True

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]




