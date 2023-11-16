from odoo import models, fields, _
class UomCategories(models.Model):
    _name = 'sn_uom.categories'
    _description = 'Catégories des unités de mesures'

    
    company_id = fields.Many2one(
        string='Company', 
        comodel_name='res.company', 
        required=True, 
        default=lambda self: self.env.user.company_id
    )
    
    name = fields.Char( string='Nom', required=True )
    
    _sql_constraints = [
        (
            'name_unique',
            'unique (name)',
            _('Nom de catégorie de mesure doit être unique')
        ) ]

    
    