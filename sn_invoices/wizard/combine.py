from odoo import api, fields, models, _


    
class wiz_selected_commandes(models.TransientModel):

    _name = 'sn_sales.commandes_selected.wiz'
    def _default_cmd_ids(self):
        cmd_ids = self._context.get('active_model') == 'sn_sales.commandes' and self._context.get('active_ids') or []
        
        return [(0, 0, {'cmd_id': cmd.id, 
                    'cmd_name':cmd.name,
                    'cmd_date':cmd.display_date,
                    # 'company_id':cmd.company_id,
                    'partner_id':cmd.partner_id.id,
                    'client_name':cmd.partner_id.name,
                    'facture_name':cmd.facture_name,
                    'count_lines':cmd.commande_lines_count
                    })
            for cmd in self.env['sn_sales.commandes'].browse(cmd_ids) ]
        
    is_momken = fields.Boolean("Is Possible",compute='verify_please',default=True)
    motif = fields.Char("Motif",compute='verify_please',default='' ) 
    selected_commandes_ids = fields.One2many('sn_sales.combine_commandes.wiz',"wizard_id" , string='Selected cmds',  default=_default_cmd_ids)
    selected_commandes_ids_count = fields.Integer('ids count', compute='_compute_lines_count' ,default=0)
   
    @api.depends('selected_commandes_ids')
    def verify_please(self):
        motif=""
        clients_ids=set()
        for cmd in self.selected_commandes_ids:
            clients_ids.add(cmd.partner_id)
            motif += "{} est attaché à la facture {} <br/>".format(cmd.cmd_name,cmd.facture_name) if cmd.cmd_id.facture_image>0 else "" 
            motif += "Nombre de ligne = 0 pour la commande {} <br/>".format(cmd.cmd_name) if cmd.count_lines==0 else ""
        
        motif += "Les commandes sélectonnés n'appartiennent pas au même client<br/>" if len(clients_ids)>1 else ""
        self.motif=motif
        self.is_momken=len(motif)==0 and len(self.selected_commandes_ids)>1
        
    @api.depends('selected_commandes_ids')
    def _compute_lines_count(self):
        for rec in self:
            rec.selected_commandes_ids_count = len(rec.selected_commandes_ids)
    def do_groupe(self):

        filb_values =[]
        ids=[]
        for cmd in self.selected_commandes_ids:
          ids.append(cmd.cmd_id.id)  
          for line in cmd.cmd_id.commande_lines:
            filb_values.append((0, 0, {'name': line.name,                               
                               'product_id': line.product_id.id,
                               'sequence': line.sequence,
                               'price_unit': line.price_unit,
                               'price_total': line.price_total,
                               'remise_taux': line.remise_taux,
                               'remise_mta': line.remise_mta,
                               'product_code': line.product_code,
                               'qty': line.qty,                               
                               'product_image': line.product_image,
                               'display_type': line.display_type,
                               }))

        ctx = {
            'default_commande_origin': ids[0],
            'default_extra_commande_origin': ids[1:],
            'default_partner_id': self.selected_commandes_ids[0].partner_id,
            'default_creation_date': fields.Date.today(),
            'default_tva_exist': True,
            'default_tva_taux': 19.0,
            'default_remise_exist': False,
            'default_remise_taux': 5.0,
            'default_remise_mta': 100.0,
            'default_remise_methode': 'taux',
            'default_remise_applied_on': 'global',
            'default_remise_valeur': 5.0,

            #'default_company_id': self.env['res.company']._company_default_get('sn_sales.commandes'),
            # 'default_company_id': self.selected_commandes_ids[0].company_id,

            'default_product_name_editable': self.env['ir.config_parameter'].sudo().get_param('sn_sales.product_name_editable'),

            'default_facture_lines': filb_values,
            'default_code_article_exist': False,
        }

        form_view_id = self.env.ref('sn_invoices.view_facture_form').ids
        return {
            'views': [[form_view_id, 'form']],
            'name': _('Facture'),
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': form_view_id,
            'res_model': 'sn_invoices.invoices',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': ctx,
        }

   
class wiz_combine_commandes(models.TransientModel):
    _name = 'sn_sales.combine_commandes.wiz'
    _description = 'Cammandes combined'

    wizard_id = fields.Many2one('sn_sales.commandes_selected.wiz', string='Wizard', required=True,)
    cmd_id = fields.Many2one('sn_sales.commandes', string='Cmds', required=True)
    #commande_lines=fields.One2many('sn_sales.commande.lines', 'commande_id', related='cmd_id.commande_lines')

    cmd_name = fields.Char('Numéro')
    cmd_date= fields.Date('Date')
    facture_name = fields.Char(string='Facture' )
    partner_id = fields.Integer('partner_id')
    client_name = fields.Char("Client")
    # company_id = fields.Integer('company_id')
    count_lines = fields.Integer('Nbr Lignes')
    