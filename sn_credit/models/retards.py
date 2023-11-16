from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class NticCreditsRetards(models.Model):
    _name = "sn_credit.retards"
    _description = 'Retards cases'

    command_id = fields.Many2one('sn_sales.commandes', string='Commande Reference',
                               required=True, ondelete='cascade',
                               index=True,copy=False)

    retard_lines_ids = fields.One2many(
        string='retard_lines',
        comodel_name='sn_credit.retards.lines',
        inverse_name='retard_id',
    )

    mta_tot_months_retard = fields.Float("Montant", digits="montant")

    # ex: 1/2020,2/2020
    # months_in_retard = fields.Char("Mois déclarés en retard")

    commande_id_generated=fields.Integer("Commande liée",default=0)

class NticCreditsRetardsLines(models.Model):
    _name = "sn_credit.retards.lines"
    _description = 'Details of retards cases'

    retard_id = fields.Many2one('sn_credit.retards', string='retard Reference',
                               required=True, ondelete='cascade',
                               index=True,copy=False)
    month = fields.Integer(string='month'    )
    year = fields.Integer(string='year'    )
    montant = fields.Float("Montant", digits="montant")




