from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
#import datetime
#from dateutil.relativedelta import relativedelta
#from odoo.exceptions import ValidationError

class wiz_invoices_commandes(models.TransientModel):
    _inherit = 'sn_sales.commandes.wiz1'

  
#####
#####  NOT USED
#####
    with_facture = fields.Selection(
        string='Avec/Sans Facture',
        selection=[
            ('all', 'Tous'), 
            ('with', 'Avec Facture'), 
            ('without', 'Sans Facture')],
        default='all' )
 
    @api.onchange('with_facture')
    def clear_invoices_ids(self):
        self.commandes_ids=[]

    