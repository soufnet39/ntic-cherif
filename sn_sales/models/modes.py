from odoo import models, fields, api

class MyModePaiement(models.Model):
    _name = 'sn_sales.modes_paiement'
    _description = 'Modes de paiement'
    _order = "sequence"

    name = fields.Char(string="Mode", required=True, )
    sequence = fields.Integer(required=True, default=10)
    # is_cash = fields.Boolean("es Espèce?", default=False)
    isdefault = fields.Boolean("Défault?", default=False)
    nature = fields.Selection(  string='Nature', selection=[('cash', 'Espèce'), ('cheque', 'Chèque')]  )

    _sql_constraints = [
        ('mode_paiement_unique', 'unique (name)', 'Mode de paiement éxiste déjà!'),
    ]


    # @api.onchange('is_cash')
    # def _onchange_field(self):
    #     if self.is_cash:
    #         halats=self.env["sn_sales.modes_paiement"].search([("is_cash","=",True),("id","!=",self._origin.id)])
    #         if halats:
    #            halats.update({'is_cash':False})


class MyCondPaiementsTerm(models.Model):
    _name='sn_sales.methodes_paiement'
    _description = 'Méthodes de paiement'
    _order = "sequence"

    name = fields.Char(string='Méthode de paiement', translate=True, required=True)
    sequence = fields.Integer(required=True, default=10)
    isdefault = fields.Boolean("Défault?", default=False)
    _sql_constraints = [
        ('methode_paiement_unique', 'unique (name)', 'Méthode de paiement éxiste déjà!'),
    ]

class MyCondPaiementsTerm(models.Model):
    _name='sn_sales.conditions_vente'
    _description = 'Conditions de vente'
    _order = "sequence"

    name = fields.Char(string='Condition de vente', translate=True, required=True)
    sequence = fields.Integer(required=True, default=10)
    isdefault = fields.Boolean("Défault?", default=False)
    _sql_constraints = [
        ('condition_vente_unique', 'unique (name)', 'Terme de Condition de vente éxiste déjà!'),
    ]
class MyCondPaiementsTerm(models.Model):
    _name='sn_sales.validities_offre'
    _description = 'Validités des offres'
    _order = "sequence"

    name = fields.Char(string="Validité de l'offre", translate=True, required=True)
    sequence = fields.Integer(required=True, default=10)
    isdefault = fields.Boolean("Défault?", default=False)
    _sql_constraints = [
        ('validite_offre_unique', 'unique (name)', "Terme de validité d'offre éxiste déjà!"),
    ]

