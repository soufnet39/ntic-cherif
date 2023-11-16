from odoo import api, models, fields

class BoxesExpensesOperationsModule(models.Model):
    _inherit = 'sn_boxes.operations'

    expense_category = fields.Many2one(comodel_name="sn_expenses.categories", string="Catégorie")