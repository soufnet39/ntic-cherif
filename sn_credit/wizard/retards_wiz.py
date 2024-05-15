from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError
import datetime
from dateutil.relativedelta import relativedelta
from odoo.osv import osv

## To control the wizar model
class wiz_tardations(models.TransientModel):
    _name = 'sn_credit.wiz_tardations'

    name = fields.Char('Name', default='default')
    retards_ids = fields.One2many('sn_credit.retards.wiz',"wiz_retard_id", string='Retards')
   

    def print_retards(self):
        if (len(self.retards_ids)==0):
               raise ValidationError(_('Trouvez les cas en retard d abord'))
        return self.env.ref('sn_credit.action_report_retarts_touves').report_action(self)



    def fetch_retards(self):
        # if (len(self.retards_ids)>0):
        #     raise ValidationError(_('Retards déjà Calculés'))
        self.retards_ids = [(5,0,0)]
        self.env.cr.execute("""
                SELECT c.id,c.name,c.partner_id,c.amount_rest,p.display_name,c.contrat,p.ccp_cle
                FROM public.sn_sales_commandes c
                lEFT JOIN public.sn_sales_partner p on p.id = c.partner_id 
                WHERE 
                c.company_id=%s and c.amount_rest>500 
                and c.date_end < (now()- interval '2 month') and 
                c.operation_type='command' and
                not COALESCE(c.is_considered_as_retard,False)
                order by c.id
            """ % (self.env.company.id))

        retards = self.env.cr.fetchall()
        
        tmp_lines = []
        if retards:
            for rtd in retards: 
                tmp_lines.append((0, 0, {
                                'command_id' : rtd[0], 
                                'command_name' : rtd[1], 
                                'partner_id' : rtd[2], 
                                'amount_rest' :rtd[3], 
                                'partner_name' :rtd[4]+'/'+str(rtd[6])  ,
                                'contrat' :rtd[5]  
                                    }))
                                #'addad_monthes' :rtd[4],
        else:
            raise ValidationError(_('Pas de retard'))

        self.retards_ids = tmp_lines

class retardsWiz(models.TransientModel):
    _name = 'sn_credit.retards.wiz'
    _description = 'Retards cases temporaire'

    name = fields.Char('Name', default='default')
    wiz_retard_id = fields.Many2one('sn_credit.wiz_tardations', string='retard Reference',
                               required=True, ondelete='cascade',
                               index=True,copy=False)
    command_id = fields.Integer("command id",readonly=True) # Instead on many2one
    contrat = fields.Integer("contrat",readonly=True) # Instead on many2one
    command_name = fields.Char("B.C N°",readonly=True) # Instead on many2one
    partner_name = fields.Char("Client",readonly=True)
    partner_id = fields.Integer("Client id",readonly=True)
    amount_rest = fields.Float("Montant", digits="montant",readonly=True)

    def traite_retard(self):
        qr= "select is_generated_from_retard from public.sn_sales_commandes where id=%s"
        self.env.cr.execute(qr % (self.command_id))
        query_result = self.env.cr.fetchone()
        if (query_result and query_result[0]):
            raise UserError(_('Commande déjà Traitée..')) 
                       
        query="SELECT id FROM public.sn_sales_product where name LIKE '%Retard%' and name LIKE '%...%'"
        self.env.cr.execute(query)
        query_result = self.env.cr.fetchone()
        if (not query_result):
            raise UserError(_('Je trouve pas l article ... Retard ...')) 


        selected_cmd_id = self.env.context["selected_cmd_id"]
        selected_partner_id = self.env.context["selected_partner_id"]
        selected_cmd_name = self.env.context["selected_cmd_name"]
        selected_montant = self.env.context["selected_montant"]
        selected_contrat = self.env.context["selected_contrat"]

        filb_values =  {'name': 'Retard de bon n° '+selected_cmd_name,
                               'product_id':  query_result[0], # convention code retard
                               'qty': 1,
                               'price_unit': selected_montant,
                               'sequence': 10,
                               'price_total': selected_montant                        
                        }

        ctx={
                'default_partner_id': selected_partner_id,
                'default_creation_date': fields.Date.today(),
                'default_contrat': selected_contrat,
                'default_state': 'confirmed',
                'default_operation_type':'command',
                'default_commande_lines': [(0, 0,filb_values)],

                'default_is_generated_from_retard': True,
                'default_retard_source_id': selected_cmd_id,
                'default_retard_source_name': selected_cmd_name,
            }

        form_view_id = self.env.ref('sn_sales.view_commande_form').ids
        ## delete selected line
        #self.retards_ids = [(2,self.id)]
        return {
            'views': [[form_view_id, 'form']],
            'name': '/',
            'view_mode': 'form',
            'view_id': form_view_id,
            'res_model': 'sn_sales.commandes',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': ctx
        }

