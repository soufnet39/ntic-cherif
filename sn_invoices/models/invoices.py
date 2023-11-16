from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons.sn_base.models.chiffres2letters import hawel
from odoo.addons.sn_base.models.chiflet_ar import chiflet

class NticInvoices(models.Model):
    _name = "sn_invoices.invoices"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Ntic invoices"
    _order = 'name desc,id desc, creation_date desc'

    def chiflet(self, mta):
        print_lg=self.env['ir.config_parameter'].sudo().get_param('sn_sales.print_language')
        lg = self.env.user.lang
        if print_lg == 'client':
            lg = self.partner_id.lang
        if lg in ["ar_SY"]:
            return chiflet(mta)
        else:
            return hawel(mta, self.company_id.currency_id.name)

    @api.depends('facture_lines.price_total', 'remise_exist', 'remise_applied_on', 'remise_methode', 'remise_taux',
                 'remise_mta', 'tva_exist', 'tva_taux','mode_paiement_id','ret_gar_exist','ret_gar_taux')
    def _amount_all(self):
        for facture in self:
            amount_ht = amount_ttc = amount_tva = amount_timbre = remise_valeur = amount_ht_before_remise = 0.0
            compteur = 0

            for line in facture.facture_lines:
                amount_ht_before_remise += line.price_total
                if facture.remise_exist and facture.remise_applied_on == 'article':
                    if facture.remise_methode == 'taux':
                        amount_ht += line.price_total * (1 - line.remise_taux / 100)
                        remise_valeur += line.price_total * line.remise_taux / 100
                    if facture.remise_methode == 'mta':
                        amount_ht += line.price_total - line.remise_mta
                        remise_valeur += line.remise_mta
                if facture.remise_exist and facture.remise_applied_on == 'global' or not facture.remise_exist:
                    amount_ht += line.price_total

                compteur += 1

            facture.facture_lines_count = compteur

            if facture.remise_exist and facture.remise_applied_on == 'global':
                if facture.remise_methode == 'taux':
                    remise_valeur = amount_ht * facture.remise_taux / 100
                    amount_ht = amount_ht - remise_valeur
                if facture.remise_methode == 'mta':
                    remise_valeur = facture.remise_mta
                    amount_ht = amount_ht - remise_valeur

            
            if facture.tva_exist:
                amount_tva = amount_ht * (facture.tva_taux / 100)

            if facture.mode_paiement_id:
                if facture.mode_paiement_id.nature=='cash':
                    amount_timbre=min((amount_ht + amount_tva)/100,2500.00) 

            amount_ttc_before_retenue = amount_ht + amount_tva +amount_timbre
            amount_retenue = amount_ttc_before_retenue * facture.ret_gar_taux/100 if facture.ret_gar_exist else 0.0
            amount_ttc =  amount_ttc_before_retenue-amount_retenue
                           
            facture.update({
                'remise_valeur': remise_valeur,
                'amount_ht_before_remise': amount_ht_before_remise,
                'amount_ht': amount_ht,
                'amount_tva': amount_tva,
                'amount_timbre': amount_timbre,
                'amount_ttc_before_retenue': amount_ttc_before_retenue,
                'amount_retenue': amount_retenue,
                'amount_ttc': amount_ttc
            })

    @api.depends('price_unit', 'qty', 'remise_taux', 'tva_exist', 'tva_taux')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.remise_taux or 0.0) / 100.0)
            mta = line.qty * price
            line.update({'price_total': mta})

    def get_delivery_confirmed_by_default_settings(self):
        for line in self:
            line.delivery_confirmed = self.env['ir.config_parameter'].sudo().get_param('sn_sales.delivery_confirmed_by_default')

    proforma_origin = fields.Integer(string='Proforma Ref', copy=False, default=0, readonly=True)
    commande_origin = fields.Integer(string='Commande Ref', copy=False, default=0, readonly=True)
    # avoir_source : facture original annnulée 
    avoir_source = fields.Integer(string='Facture Ref', copy=False, default=0, readonly=True)
    # avoir_target: Facture avoir généré
    avoir_target = fields.Integer(string='Facture Ref', copy=False, default=0, readonly=True)
    
    extra_commande_origin = fields.One2many('sn_sales.commandes','extra_id')

    name = fields.Char(string='Facture: ', required=True, copy=False, index=True, default='/', )
    facture_lines = fields.One2many('sn_invoices.invoices.lines', 'facture_id', string='Un article à facturer', copy=True, )
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('canceled', 'Annullé'),
        ('avoir', 'Avoir') ],
        string='Etat', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default='draft')

    # STORE = FALSE ###################################
    numero_updatable = fields.Boolean(string="Numero Modifiable", store=False, default=False)
    ###################################################

    creation_date = fields.Date(string='Date de création', required=True, index=True, 
                                  default=lambda self:fields.Date.today() )

    # date saved when state is done
    confirmation_date = fields.Date(string='Date',  index=True,default=lambda self:fields.Date.today())

    user_id = fields.Many2one('res.users', string='Vendeur', index=True, track_visibility='onchange', track_sequence=2, default=lambda self: self.env.user)

    partner_id = fields.Many2one('sn_sales.partner', string='Client', required=True,index=True, track_visibility='always', track_sequence=1,domain=[('is_customer', '=', True)] )
    tarification = fields.Selection('Tarification', related='partner_id.tarification')
    list_prix = fields.Many2one("sn_sales.pricelist", string="Liste de prix", related='partner_id.list_prix')
    # pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True, readonly=True,
    #                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)


    # invoice_ids = fields.Many2many("account.invoice", string='Invoices', compute="_get_invoiced", readonly=True, copy=False)

    # default note could be saved as config parameter for all orders
    note = fields.Text('Note', default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_invoices.facture_note_default') )

    #### TVA ##################################################################################################
    tva_exist = fields.Boolean(string="Tva Exist",
                               default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                   'sn_sales.tva_exist'))
    tva_taux = fields.Float(string="Taux TVA", required=False,  default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.tva_taux'))
    ###########################################################################################################

    #### Remise ##################################################################################################
    remise_exist = fields.Boolean(string="Remise Exist",
                                  default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                      'sn_sales.remise_exist'))
    remise_taux = fields.Float(string='Taux de Remise', default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                   'sn_sales.remise_default_taux'))
    remise_mta = fields.Float(string='Montant de remise', default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                  'sn_sales.remise_default_mta'))
    remise_methode = fields.Selection(string="Methode de remise", selection=[('taux', 'Taux'), ('mta', 'Montant')],
                                      required=True,
                                      default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                          'sn_sales.remise_methode', 'taux'))
    remise_applied_on = fields.Selection(string="Remise à appliquer",
                                         selection=[('article', 'Par article'), ('global', 'En global')],
                                         required=True,
                                         default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                             'sn_sales.remise_applied_on', 'global'))
    remise_valeur = fields.Float(string="Remise %", store=True, digits="montant", readonly=True, compute='_amount_all',  )
    amount_ht_before_remise = fields.Float(string="Montant HT", digits="montant",store=True,readonly=True, compute='_amount_all')
    timbre_applicable = fields.Boolean(string="Timbre applicable", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.timbre_exist'))
    ###########################################################################################################

    # Monetary
    amount_ht = fields.Float(string='Montant HT', digits="montant", store=True, readonly=True, compute='_amount_all', track_visibility='onchange', track_sequence=5)
    amount_ht_signed = fields.Float(string="Total HT", digits="montant",compute="_compute_signed",store=True)
    # Monetary
    amount_timbre = fields.Float(string='Timbre',digits="montant", store=True, readonly=True, compute='_amount_all')
    amount_timbre_signed = fields.Float(string="Timbre", digits="montant",compute="_compute_signed",store=True)
    amount_tva = fields.Float(string='TVA', digits="montant", store=True, readonly=True, compute='_amount_all')
    amount_tva_signed = fields.Float(string="TVA", digits="montant",compute="_compute_signed",store=True)
    # Monetary
    amount_ttc = fields.Float(string='Total TTC',digits="montant", store=True, readonly=True, compute='_amount_all', track_visibility='always', track_sequence=6)
    amount_ttc_signed = fields.Float(string="Total TTC", digits="montant",compute="_compute_signed",store=True)
    # payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')

    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('sn_invoices.invoices'))

    product_name_editable = fields.Boolean(string="Désignation editable",  default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.product_name_editable')    )

    facture_lines_count = fields.Integer('Nombre de lignes', default=0)

    # uom_exist = fields.Boolean(string="Uom exist",
    #                            default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
    #                                'sn_sales.uom_exist'))
    code_article_exist = fields.Boolean(string="Code article exist",
                                        default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                            'sn_sales.code_article_exist'))

    mode_paiement_id = fields.Many2one('sn_sales.modes_paiement', string="Mode de paiement")
    mode_paiement_nature = fields.Selection(string='nature',  related='mode_paiement_id.nature' , store=False)
    cheque_info = fields.Char( string='Chèque info.' )
    ########################@RETENUE DE GARANTIE
    ret_gar_exist = fields.Boolean(string="Garantie Existe", default=False)
    ret_gar_taux = fields.Float(string='Taux de Garantie', default=5.0)
    amount_retenue = fields.Float(string="Retenue de Garantie", digits="montant",store=True,readonly=True, compute='_amount_all')
    amount_ttc_before_retenue = fields.Float(string="Montant Avant Retenue", digits="montant",store=True,readonly=True, compute='_amount_all')

    @api.depends('amount_ttc','amount_tva','amount_timbre','amount_ht', 'state')
    def _compute_signed(self):
        for fct in self:
            sens= -1 if fct.state == 'avoir' else 1
            fct.amount_ttc_signed = sens*fct.amount_ttc
            fct.amount_ht_signed = sens*fct.amount_ht
            fct.amount_timbre_signed = sens*fct.amount_timbre
            fct.amount_tva_signed = sens*fct.amount_tva
            

    def action_confirm(self):
        qtys = sum(l.qty for l in self.facture_lines)
        if qtys <= 0:
            raise UserError(_('Les quantités sont nuls, Pas de confirmation '))
            return False
        else:
            self.update({
                'state': 'confirmed',
                'confirmation_date':  fields.Date.today()  #, self.creation_date
            })
            return True

    def action_cancel(self):
        self.update({
            'state': 'canceled',
        })
        return True
    def action_to_avoir(self):
        self = self.with_context({'default_avoir_source': self.id,                                  
                                  'is_avoir':True,
                                  'name':self.name,
                                  'date':self.confirmation_date })
        avoir_copy=self.copy()
        if avoir_copy:
            form_view_id = self.env.ref('sn_invoices.view_facture_form').ids        
            context = dict(self.env.context)          
            return {
                'views': [[form_view_id, 'form']],
                'name': _('Facture'),
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': form_view_id,
                'res_model': 'sn_invoices.invoices',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': avoir_copy.id,
                'context': context,
            }
            
        return False

    def action_draft(self):
        self.update({
            'state': 'draft',
            'creation_date': fields.Date.today(),
            'confirmation_date': fields.Date.today(),
        })
        return True

    def go2document(self):
        doc = self.env.context.get('doc')
        docs = doc + ('s' if doc=='commande' else '')
        origin = self.proforma_origin if doc == 'proforma' else self.commande_origin
        piece_ref = self.env['sn_sales.'+docs].search_count([('id', '=', origin)])
        if piece_ref>0:
            form_view_id = self.env.ref('sn_sales.view_'+doc+'_form').ids
            return {
                'views': [[form_view_id, 'form']],
                'name': _(doc),
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': form_view_id,
                'res_model': 'sn_sales.'+docs,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': origin
            }
        else:
            if doc=='proforma':
                self.proforma_origin=0
            if doc=='commande':
                self.commande_origin=0
            message = _(doc.capitalize()+' en relation non trouvée!.. Peut être supprimée.. Cette relation sera désormais déconnectée')
            title= _('Problème de liaison entre pièces')

            return self.env['sn_base.message_wizard'].message(title, message)

    @api.model
    def create(self, vals):
        #raise UserError(self.env.context.get('default_avoir_source'))
        
        is_avoir=self.env.context.get('is_avoir')
        gwr = 'avoir' if is_avoir else 'facture'
        prefix = 'AVR/%(year)s/' if is_avoir else 'FCT/'
        next_one = self.env['ir.sequence'].get(gwr)
        if not next_one:
            dict = {"prefix": prefix,
                    "code": gwr,
                    "name": gwr,
                    "active": True,
                    "padding": 3,
                    "implementation": "standard",
                    }
            self.env['ir.sequence'].create(dict)
            next_one = self.env['ir.sequence'].next_by_code(gwr)
        vals['name'] = next_one

        record = super(NticInvoices, self).create(vals)
        # check config var ´facture_confirmed_by_default´
        
        #if vals.get('creation_date'):
        #    if self.env['ir.config_parameter'].sudo().get_param('sn_invoices.facture_confirmed_by_default'):
        #        record.update({'state': 'confirmed','confirmation_date': vals['creation_date']}) # , fields.Date.today()
        if is_avoir:
            record.update({'state':'avoir',
                           'avoir_source':self.env.context.get('default_avoir_source'),
                           'note':'Avoir sur Factue N°: '+self.env.context.get('name')+' du: '+self.env.context.get('date').strftime("%d/%m/%Y")})
                           
            for l in record.facture_lines:
                l.update({'name': 'Retour marchandise \n '+l.name})
        proforma_original = self.env.context.get('default_proforma_origin')
        if record and proforma_original and proforma_original > 0:
            prf = self.env['sn_sales.proforma'].search([('id', '=', proforma_original)])
            if prf:
                prf.write({'facture_image': record.id})

        commande_original = self.env.context.get('default_commande_origin')
        extra_commande_original = self.env.context.get('default_extra_commande_origin') or []
        extra_commande_original.append(commande_original)
        if record and commande_original and commande_original > 0:
            prf = self.env['sn_sales.commandes'].search([('id', 'in', extra_commande_original)])
            if prf:
                prf.write({'facture_image': record.id,'facture_name':record.name})
        return record

    def print_facture(self):
        # self.filtered(lambda s: s.state == 'draft').write({'state': 'confirmed'})
        return self.env.ref('sn_invoices.action_facture_report').report_action(self)


# ########################################################################################################################
class NticSaleOrderLines(models.Model):
    _name = 'sn_invoices.invoices.lines'
    _description = 'Ntic Facturation Lines'
    _order = 'facture_id, sequence, id'

    @api.depends('product_id', 'facture_id.state')
    def _compute_product_updatable(self):
        for line in self:
            if line.state in ['confirmed', 'cancel']:
                line.product_updatable = False
            else:
                line.product_updatable = True

    @api.depends('price_unit', 'qty')
    def _haseb(self):
        for line in self:
            if line.display_type=="composed" or (not line.display_type):
                line.price_total = line.price_unit * line.qty
            else:
                line.price_total = 0

    facture_id = fields.Many2one('sn_invoices.invoices', string='Facturation Reference',
                               required=True, ondelete='cascade',
                               index=True, copy=False, readonly=True)
    name = fields.Text(string='Désignation', required=True)

    sequence = fields.Integer(string='Sequence', default=10)

    price_unit = fields.Float('Unit Price', digits="montant", required=True, default=0.0)

    # #Monetary
    price_total = fields.Float(compute='_haseb', digits="montant", string='Total', readonly=True, store=True,)

    remise_taux = fields.Float(string='Remise %',  )
    remise_mta = fields.Float(string='Remise',  )

    product_id = fields.Many2one('sn_sales.product', string='Product', domain=[('sale_ok', '=', True)],
                                 change_default=True, ondelete='restrict')
    product_code = fields.Char(string="Code", related='product_id.code', required=False,)

    qty = fields.Float(string='Qte.', required=True, default=1.0, digits="Quantity" )

    product_image = fields.Binary('Product Image', related="product_id.image", store=False, readonly=False)

    user_id_id = fields.Many2one(related='facture_id.user_id', store=True, string='Salesperson', readonly=True)

    company_id = fields.Many2one(related='facture_id.company_id', string='Company', store=True, readonly=True)

    facture_partner_id = fields.Many2one(related='facture_id.partner_id', store=True, string='Customer')

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note"),
        ('composed', "Composé")],  help="UX Raisons.")

    @api.onchange('product_id')
    def affect_name_to_designation(self):
        if not self.product_id.id:
            return

        price = 0
        libelle = ''
        if self.facture_id.tarification=='standard':
            price = self.product_id.default_price
        if self.facture_id.tarification == 'special':
            if self.facture_id.list_prix and self.product_id.pricelist_item_ids:
                for prix in self.product_id.pricelist_item_ids:
                    if prix.pricelist_id.id == self.facture_id.list_prix.id:
                        price = prix.fixed_price
                        libelle= prix.pricelist_id.name


        self.price_unit=price
        self.price_list_libelle=libelle
        self.name = self.product_id.name