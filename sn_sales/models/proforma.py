from odoo import models, fields, api, _
from datetime import timedelta
from odoo import exceptions
from odoo.addons.sn_base.models.chiffres2letters import hawel
from odoo.addons.sn_base.models.chiflet_ar import chiflet


class NticProforma(models.Model):
    _name = "sn_sales.proformas"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Ntic Proformas"
    _order = 'id desc, creation_date desc'




    def chiflet(self,mta):
        lg=self.env.user.lang
        if lg in ["ar_SY"]:
            return chiflet(mta)
        else:
            return hawel(mta, self.company_id.currency_id.name)

    # @api.depends('validity_days', 'validity_exist')
    # def _validity_date(self):
    #     for proforma in self:
    #         days = proforma.validity_days
    #         if days > 0 and self.validity_exist:
    #             youm = proforma.confirmation_date if proforma.state == 'confirmed' else proforma.creation_date
    #             proforma.update({
    #                 'validity_date': fields.Date.to_string( youm + timedelta(days)),
    #             })


    def _default_confirmation_date(self):
        if self.env['ir.config_parameter'].sudo().get_param('sn_sales.proforma_confirmed_by_default')  :
           return  fields.Date.today()

    @api.depends('proforma_lines')
    def _compute_lines_count(self):
        for rec in self:
            rec.proforma_lines_count = len(rec.proforma_lines)

    @api.depends('proforma_lines.price_total','remise_exist','remise_applied_on', 'remise_methode','remise_taux','remise_mta', 'tva_exist', 'tva_taux','mode_paiement_id')
    def _amount_all(self):
        for proforma in self:
            amount_ht = amount_tva = amount_timbre = remise_valeur = amount_ht_before_remise = 0.0

            for line in proforma.proforma_lines:
                amount_ht_before_remise += line.price_total
                if proforma.remise_exist and proforma.remise_applied_on=='article':
                    if proforma.remise_methode == 'taux':
                        amount_ht += line.price_total*(1-line.remise_taux/100)
                        remise_valeur += line.price_total*line.remise_taux/100
                    if proforma.remise_methode == 'mta':
                        amount_ht += line.price_total-line.remise_mta
                        remise_valeur += line.remise_mta
                if proforma.remise_exist and proforma.remise_applied_on=='global' or not proforma.remise_exist:
                    amount_ht += line.price_total

            if proforma.remise_exist and proforma.remise_applied_on == 'global':
                if proforma.remise_methode == 'taux':
                    remise_valeur = amount_ht * proforma.remise_taux/100
                    amount_ht = amount_ht-remise_valeur
                if proforma.remise_methode == 'mta':
                    remise_valeur = proforma.remise_mta
                    amount_ht=amount_ht-remise_valeur

            if proforma.tva_exist:
                amount_tva = amount_ht * (proforma.tva_taux / 100)

            if proforma.mode_paiement_id:
                if proforma.mode_paiement_id.nature=='cash':
                    amount_timbre=min((amount_ht + amount_tva)/100,2500.00)

            proforma.update({
                'remise_valeur': remise_valeur,
                'amount_ht_before_remise': amount_ht_before_remise,
                'amount_ht': amount_ht,
                'amount_tva': amount_tva,
                'amount_timbre': amount_timbre,
                'amount_ttc': amount_ht + amount_tva + amount_timbre,
            })

    @api.model
    def _default_state(self):
        if self.env['ir.config_parameter'].sudo().get_param('sn_sales.proforma_confirmed_by_default'):
            return 'confirmed'
        return 'draft'


    @api.depends(  'price_unit' , 'qty','remise_taux','tva_exist', 'tva_taux')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.remise_taux or 0.0) / 100.0)
            mta = line.qty * price
            line.update({'price_total': mta})


    commande_image= fields.Integer(string="Commande Réf.", readonly=True, copy=False)
    facture_image= fields.Integer(string="Facture Réf.", readonly=True, copy=False)

    name = fields.Char(string='Facture Proforma', required=True, copy=False, index=True,default='/', )
    name_updatable = fields.Boolean(string="Numero Modifiable",store=False, default=False  )
    proforma_lines = fields.One2many('sn_sales.proforma.lines', 'proforma_id', string='Un article', copy=True, )
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('canceled', 'Annulée'),],
        string='Etat', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default=_default_state )

    creation_date = fields.Date(string='Création', index=True,  copy=False, default=lambda self:fields.Date.today() )
    # date saved when state is confirmed
    confirmation_date = fields.Date(string='Date',  index=True, copy=False,default=_default_confirmation_date)

    is_expired = fields.Boolean( string="Eexpiré") #compute='_compute_is_expired',

    user_id = fields.Many2one('res.users', string='Vendeur', index=True, track_visibility='onchange', track_sequence=2, default=lambda self: self.env.user)

    partner_id = fields.Many2one('sn_sales.partner', string='Client', required=True, index=True,
                domain=[('is_customer', '=', True)],
                track_visibility='always',
                track_sequence=1, )
    tarification = fields.Selection('Tarification', related='partner_id.tarification')
    solvency = fields.Selection('Solvency', related='partner_id.solvency')
    list_prix = fields.Many2one("sn_sales.pricelist", string="Liste de prix", related='partner_id.list_prix')

    note = fields.Text('Note', default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.proforma_note_default') )

    #### TVA/timbre ##################################################################################################
    tva_exist = fields.Boolean(string="Tva Exist", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.tva_exist'))
    tva_taux = fields.Float(string='Taux TVA',
                            digits="TVA",
                            default=lambda self: self.env['ir.config_parameter'].sudo().get_param(  'sn_sales.tva_taux'))
    #timbre_applicable = fields.Boolean(string="Timbre applicable", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.timbre_exist'))
    ###########################################################################################################

    #### REMISE ###############################################################################################
    remise_exist = fields.Boolean(string="Remise Exist", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_exist'))
    remise_taux = fields.Float(string='Taux de Remise',
                               digits="Remise Taux",
                               default= lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_default_taux'))
    remise_mta = fields.Float(string='Montant de remise',
                              digits="Remise Montant",
                              default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_default_mta'))
    remise_methode = fields.Selection(string="Methode de remise", selection=[('taux', 'Taux'), ('mta', 'Montant')],
                                     required=True,
                                      default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_methode','taux'))
    remise_applied_on = fields.Selection(string="Remise à appliquer",
                                         selection=[('article', 'Par article'), ('global', 'En global')],
                                         required=True,
                                         default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_applied_on','global'))
    remise_valeur = fields.Float(string="Remise %",
                                 digits="montant",
                                 store=True, readonly=True, compute='_amount_all' )
    amount_ht_before_remise = fields.Float(string="Montant HT",
                                           digits="montant",
                                           store=True,  readonly=True, compute='_amount_all'  )

    ###########################################################################################################

    # Monetary
    amount_ht = fields.Float(string='Montant HT', store=True, readonly=True, compute='_amount_all',
                             digits="montant",
                             track_visibility='onchange', track_sequence=5)
    # Monetary
    amount_tva = fields.Float(string='TVA', store=True, readonly=True,
                              digits="montant",
                              compute='_amount_all')
    # Monetary
    amount_timbre = fields.Float(string='Timbre', store=True, readonly=True,
                              digits="montant",
                              compute='_amount_all')
    # Monetary
    amount_ttc = fields.Float(string='Total TTC', store=True, readonly=True,
                              digits="montant",
                              compute='_amount_all', track_visibility='always', track_sequence=6)

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sn_sales.proformas'))

    product_name_editable = fields.Boolean(string="Désignation editable",  default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.product_name_editable')    )

    proforma_lines_count = fields.Integer('Nombre de lignes', default=0,compute='_compute_lines_count')


    code_article_exist = fields.Boolean(string="Code article exist",  default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.code_article_exist') )

    validity_exist = fields.Boolean(string="Date / Nbr Jours",  default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.validity_exist') )
    validity_date = fields.Date(string='Date de Validité',  copy=False, ) #compute="_validity_date"
     

    mode_paiement_id = fields.Many2one('sn_sales.modes_paiement', string="Mode de paiement", default=lambda self: self.env['sn_sales.modes_paiement'].search([('isdefault', '=', True)], limit=1, order='sequence').id )
    methode_paiement_id = fields.Many2one('sn_sales.methodes_paiement', string="Méthode de paiement", default=lambda self: self.env['sn_sales.methodes_paiement'].search([('isdefault', '=', True)], limit=1, order='sequence').id)
    condition_vente_id = fields.Many2one('sn_sales.conditions_vente', string="Condition de vente", default=lambda self: self.env['sn_sales.conditions_vente'].search([('isdefault', '=', True)], limit=1, order='sequence').id)
    validity_offre_id = fields.Many2one('sn_sales.validities_offre', string="Validité de l'offre", default=lambda self: self.env['sn_sales.validities_offre'].search([('isdefault', '=', True)], limit=1, order='sequence').id)

    # def _compute_is_expired(self):
    #     today = fields.Date.today()
    #     for proforma in self:
    #         if proforma.validity_days>0:
    #             date2comp = proforma.confirmation_date if proforma.state=='confirmed' else proforma.creation_date
    #             proforma.validity_date = date2comp + timedelta( days = proforma.validity_days)
    #             proforma.is_expired = proforma.validity_date < today
    #         else:
    #             proforma.is_expired = False

    def chiflet(self, mta):
        lg=self.env.user.lang
        if lg in ["ar_SY"]:
            return chiflet(mta)
        else:
            return hawel(mta, self.company_id.currency_id.name)

    def action_confirm(self):
        self.update({
            'state': 'confirmed',
            'confirmation_date': fields.Date.today(),
        })
        return True
    ## Overwritten totally in albelt
    def action_convert2commande(self):
        filb_values = [(0, 0, {'name': line.name,
                               'product_id': line.product_id.id,
                               'sequence': line.sequence,
                               'price_unit': line.price_unit,
                               'price_total': line.price_total,
                               'remise_taux': line.remise_taux,
                               'remise_mta': line.remise_mta,
                               'product_code': line.product_code,
                               'qty': line.qty,
                            #    'product_uom_qty': line.product_uom_qty,
                            #    'product_uom': line.product_uom.id,
                               'product_image': line.product_image,
                               'display_type': line.display_type,
                               }) for line in self.proforma_lines]

        ctx={
                'default_proforma_origin': self.id,
                'default_partner_id': self.partner_id.id,
                'default_creation_date': fields.Date.today(),
                'default_user_id': self.user_id.id,
                'default_tva_exist': self.tva_exist,
                'default_tva_taux': self.tva_taux,
                'default_remise_exist': self.remise_exist,
                'default_remise_taux': self.remise_taux,
                'default_remise_mta': self.remise_mta,
                'default_remise_methode': self.remise_methode,
                'default_remise_applied_on': self.remise_applied_on,
                'default_remise_valeur': self.remise_valeur,

                'default_company_id': self.company_id.id,
                'default_product_name_editable': self.product_name_editable,

                'default_commande_lines': filb_values,
                # 'default_uom_exist': self.uom_exist,
                'default_code_article_exist': self.code_article_exist,
            }

        form_view_id = self.env.ref('sn_sales.view_commande_form').ids
        return {
            'views': [[form_view_id, 'form']],
            'name': '/',
            'view_mode': 'form',
            'view_id': form_view_id,
            'res_model': 'sn_sales.commandes',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': ctx,
        }

        return True

    def action_cancel(self):
        self.update({
            'state': 'canceled',
        })
        return True

    def action_draft(self):
        self.update({
            'state': 'draft',
            'creation_date': fields.Date.today(),
            'confirmation_date': fields.Date.today(),
        })
        return True


    def go2commande(self):
        cmd_ref = self.env['sn_sales.commandes'].search_count([('id','=',self.commande_image)])
        if cmd_ref>0:
            form_view_id = self.env.ref('sn_sales.view_commande_form').ids
            return {
                'views': [[form_view_id, 'form']],
                'name': _('Commande'),
                'view_mode': 'form',
                'view_id': form_view_id,
                'res_model': 'sn_sales.commandes',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.commande_image

            }
        else:
            self.commande_image=0
            message = _('Commande en relation non trouvée!.. Peut être supprimée.. Cette relation sera désormais déconnectée')
            title= _('Problème de liaison entre pièces')

            return self.env['sn_base.message_wizard'].message(title, message)

    def print_proforma(self):
        #self.filtered(lambda s: s.state == 'draft').write({'state': 'confirmed'})
        return self.env.ref('sn_sales.action_report_proforma') \
            .with_context({'discard_logo_check': True}).report_action(self)

    def write(self, vals):       
        if 'proforma_lines' in vals.keys():
            for line in vals['proforma_lines']:
                if not line[2]==False:
                    if line[0]==0: # adding new article while editing
                        if line[2]['price_changed']:
                           prod = self.env['sn_sales.product'].search( [('id', '=', line[2]['product_id'])] )
                           if prod:
                              prod.update({'default_price':line[2]['price_unit']})
                              

                    if line[0]==1: # editing an article
                        if 'price_changed' in line[2].keys() and line[2]['price_changed']:
                            art_id=self.env['sn_sales.proforma.lines'].search( [('id', '=', line[1])] ).product_id.id
                            prod = self.env['sn_sales.product'].search( [('id', '=', art_id)] )
                            if prod:
                               prod.update({'default_price':line[2]['price_unit']})


        return super(NticProforma, self).write(vals)


    @api.model
    def create(self, vals):
        if 'proforma_lines' in vals.keys():
            for line in vals['proforma_lines']:
                if 'price_changed' in line[2].keys() and line[2]['price_changed']:
                    prod = self.env['sn_sales.product'].search( [('id', '=', line[2]['product_id'])] )
                    if prod:
                       prod.update({'default_price':line[2]['price_unit']})
                    
        gwr='proforma'
        next_one=self.env['ir.sequence'].get(gwr)
        if not next_one:
            dict = {"prefix": 'FP/',
                    "code": gwr,
                    "name": gwr,
                    "active": True,
                    "padding": 4,
                    "implementation": "standard",
                    }
            self.env['ir.sequence'].create(dict)
            next_one=self.env['ir.sequence'].next_by_code(gwr)
        vals['name'] = next_one
        record = super(NticProforma, self).create(vals)


        return record


# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################

class NticProformaLines(models.Model):
    _name = 'sn_sales.proforma.lines'
    _description = 'Ntic proforma Lines'
    _order = 'proforma_id, sequence, id'

    @api.depends('price_unit', 'qty')
    def _haseb(self):
        for line in self:
            line.price_total=line.price_unit*line.qty

    proforma_id = fields.Many2one('sn_sales.proformas', string='Proforma Reference',
                               required=True, ondelete='cascade',
                               index=True, readonly=True)
    company_id = fields.Many2one('res.company', 'Company', related='proforma_id.company_id')
    name = fields.Text(string='Désignation', required=True)

    sequence = fields.Integer(string='Sequence', default=10)
    recno = fields.Integer(string='N', ) # compute="recnologie"

    price_unit = fields.Float('Unit Price', required=True,
                              digits="montant",
                              default=0.0)

    price_list_libelle = fields.Char('Nom de liste de prix', default='')

    price_total = fields.Float(compute='_haseb', string='Total',
                               digits="montant",
                               readonly=True, store=True)

    remise_taux = fields.Float(string='Remise %', digits="Remise Taux",)
    remise_mta = fields.Float(string='Remise', digits="Remise Montant",  )

    product_id = fields.Many2one('sn_sales.product', string='Product',  domain=[('sale_ok', '=', True)],  change_default=True, ondelete='restrict')

    product_code = fields.Char(string="Code", related='product_id.code', required=False, )
    qty = fields.Float(string='Qte.', digits="Quantity", default=1.0)
    # product_uom_qty = fields.Float(string='Qte.',
    #                                digits="Quantity",
    #                                required=True, default=1.0)
   

    product_image = fields.Binary('Product Image', related="product_id.image", store=False, readonly=False)

    user_id_id = fields.Many2one(related='proforma_id.user_id', store=True, string='Salesperson', readonly=True)

    proforma_partner_id = fields.Many2one(related='proforma_id.partner_id', store=True, string='Customer', readonly=False)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note"), 
        ('composed', "Composé")],  help="UX Raisons.")

    price_changed = fields.Boolean( string='Approbation du nouveau prix',store=False ,default= False   )
    price_touched = fields.Boolean( string='Prix modifié',store=False ,default= False   )



    @api.onchange('product_id')
    def affect_name_to_designation(self):
        if not self.product_id.id:
            return
        # self.price_unit=self.product_id.default_price
        # self.name = self.product_id.name
        price = 0
        libelle = ''
        if self.proforma_id.tarification=='standard':
            price = self.product_id.default_price
            self.price_changed = False
            self.price_touched = False
        if self.proforma_id.tarification == 'special':
            if self.proforma_id.list_prix and self.product_id.pricelist_item_ids:
                for prix in self.product_id.pricelist_item_ids:
                    if prix.pricelist_id.id == self.proforma_id.list_prix.id:
                        price = prix.fixed_price
                        libelle= prix.pricelist_id.name

        self.price_unit=price
        self.price_list_libelle=libelle
        self.name = self.product_id.name

    @api.onchange('price_unit')
    def confirm_price_unit_changing(self):
        self.price_touched= self.price_unit!=self.product_id.default_price