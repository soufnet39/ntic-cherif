from odoo import models, fields,api, _
from odoo.exceptions import ValidationError

class UomCategories(models.Model):
    _name = 'sn_uom.uom'
    _description = 'Unités de mesures'

    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        required=True,
        default=lambda self: self.env.user.company_id
    )

    name = fields.Char( string='Abreviation', required=True )
    complete_name = fields.Char( string='Nom', required=True )

    uom_category_id = fields.Many2one(
        string='Categorie',
        comodel_name='sn_uom.categories',
        ondelete='restrict',
    )

    type_unit = fields.Selection(
        string="type d'unité",
        selection=[ ('one_unit', "Unité principale"),
                    ('division_unit', "Division d'unité"),
                    ('multiple_unit', "multiple d'unité"),
                    ],required=True
    )

    ratio = fields.Float( string='Ratio',  )

    _sql_constraints = [
        (
            'name_unique',
            'unique (name)',
            _("Nom d'unité de mesure doit être unique")
        ) ]



    @api.onchange('type_unit')
    def _onchange_field(self):
        self.ratio = 1.0

    @api.constrains('type_unit','ratio')
    def _check_one_unicity(self):
        c=0
        anomalie = False
        over_doze = False
        cat=self.uom_category_id.id
        if self.type_unit == 'one_unit':
            lista= self.env['sn_uom.uom'].search([]).read()
            for record in lista:
                if record["type_unit"] == 'one_unit' and record["uom_category_id"][0]==cat:
                    c+=1
                    anomalie=True
        over_doze = over_doze or (self.type_unit == 'division_unit' and self.ratio >1) or (self.type_unit == 'multiple_unit' and self.ratio <1)
        if over_doze:
            raise ValidationError("Veuillez vérifier bien les ratios !")
        if anomalie and c==0:
            raise ValidationError("Chaque unité doit avoir sa grandeur principale  (référence)!")
        if anomalie and c>1:
            raise ValidationError("Seulement une unité doit être principale et   unique!. Il y'en a plus que Un")

