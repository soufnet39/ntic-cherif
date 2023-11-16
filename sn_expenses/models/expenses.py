from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

class NticExpensesCategories(models.Model):

    _name = 'sn_expenses.categories'
    _description = 'Ntic Expenses Catégories'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(string="Nom", required=True, translate=True)
    complete_name = fields.Char( 'Nom Complèt', compute='_compute_complete_name',    store=True)
    parent_id = fields.Many2one('sn_expenses.categories', 'Parent', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many('sn_expenses.categories', 'parent_id', 'Child Catégories')


    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for cat in self:
            if cat.parent_id:
                cat.complete_name = '%s / %s' % (cat.parent_id.complete_name, cat.name)
            else:
                cat.complete_name = cat.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Vous ne pouvez pas créer de relation récursive.'))
        return True

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]
