from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons.sn_base.models.chiffres2letters import hawel
from odoo.addons.sn_base.models.chiflet_ar import chiflet


class NticSaleCommande(models.Model):
    _name = "sn_sales.commandes"
    _inherit = [ 'mail.thread', 'mail.activity.mixin']
    _description = "Ntic Sale Commandes"
    _order = 'id desc, creation_date desc'

    def wich_logha(self):
        return self.env['ir.config_parameter'].sudo().get_param('sn_sales.print_language')

    def chiflet(self, mta):
        print_lg=self.env['ir.config_parameter'].sudo().get_param('sn_sales.print_language')
        lg = self.env.user.lang
        if print_lg == 'client':
            lg = self.partner_id.lang

        if lg in ["ar_SY"]:
            return chiflet(mta)
        else:
            return hawel(mta, self.company_id.currency_id.name)


    def _default_confirmation_date(self):
        if (self._context.get("default_operation_type")=='command' and self.env['ir.config_parameter'].sudo().get_param('sn_sales.command_confirmed_by_default')) or  (self._context.get("default_operation_type")=='purchase' and self.env['ir.config_parameter'].sudo().get_param('sn_purchases.purchase_confirmed_by_default')) :
           return fields.Date.today()


    def _default_state(self):
        if (self._context.get("default_operation_type")=='command' and self.env['ir.config_parameter'].sudo().get_param('sn_sales.command_confirmed_by_default')) or  (self._context.get("default_operation_type")=='purchase' and self.env['ir.config_parameter'].sudo().get_param('sn_purchases.purchase_confirmed_by_default')) :
           return 'confirmed'

        return 'draft'


    @api.depends('state')
    def _creation_or_confirmation(self):
        for rec in self:
            rec.display_date= rec.confirmation_date if rec.state=='confirmed' else rec.creation_date

    @api.depends('commande_lines.price_total', 'tva_exist', 'tva_taux')
    def _amount_all(self):
        for commande in self:
            amount_ht = amount_tva  =  0.0
            for line in commande.commande_lines:
                if line.display_type not in ['line_section','line_note']:
                   amount_ht += line.price_total

            if commande.tva_exist:
                amount_tva = amount_ht * (commande.tva_taux / 100)

            commande.update({
                'amount_ht': amount_ht,
                'amount_tva': amount_tva,
                'amount_ttc': amount_ht + amount_tva ,
                'amount_ttc_sec': amount_ht + amount_tva ,
            })




    proforma_origin = fields.Integer(string='Proforma en relation',copy=False, default=0, readonly=True )

    name = fields.Char(string='Commande', required=True, copy=False, index=True, default='/',)

    name_updatable = fields.Boolean(string="Numero Modifiable", store=False, default=False)
    display_recno = fields.Boolean(string="Afficher les numéro", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.display_recno'))
    operation_type = fields.Selection([('command', 'Cmd. Vente'), ('purchase', 'Cmd Achat')],
                    string='Type operation',
                    copy=True, )

    commande_lines = fields.One2many('sn_sales.commande.lines', 'commande_id', string='Un article', copy=True, )
    commande_lines_count = fields.Integer('Nombre de lignes',store=True, compute='_compute_lines_count' ,default=0)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('canceled', 'Annulée'),],
        string='Etat', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default=_default_state)

    creation_date = fields.Date(string='Création', index=True,  copy=False , default=lambda self:fields.Date.today() )
    # date saved when state is confirmed
    confirmation_date = fields.Date(string='Confirmation',  index=True, copy=False, default=_default_confirmation_date)
    display_date= fields.Date("Date",compute="_creation_or_confirmation")

    user_id = fields.Many2one('res.users', string='Vendeur', index=True, track_visibility='onchange', track_sequence=2, default=lambda self: self.env.user)

    partner_id = fields.Many2one('sn_sales.partner', string='Client/Fournisseur',
            index=True, track_visibility='always',
            track_sequence=1,  ) #required in views

    tarification = fields.Selection('Tarification', related='partner_id.tarification')
    solvency = fields.Selection('Solvency', related='partner_id.solvency')
    list_prix = fields.Many2one("sn_sales.pricelist", string="Liste de prix", related='partner_id.list_prix')

    note = fields.Text('Note', default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.default_commande_note') )

    #### TVA ##################################################################################################
    tva_exist = fields.Boolean(string="Utiliser la Tva", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.tva_exist'))
    tva_taux = fields.Float(string="Taux TVA", digits="TVA",
                            default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.tva_taux') )
    ###########################################################################################################

    #### REMISE ###############################################################################################
    remise_exist = fields.Boolean(string="Utiliser les remises", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_exist'))
    remise_taux = fields.Float(string='Taux de remise',
                               default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_default_taux'),
                               digits="Remise Taux")
    remise_mta = fields.Float(string='Montant de remise',
                              default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.remise_default_mta')
                              , digits="Remise Montant")
    remise_methode = fields.Selection(string="Methode de remise", selection=[('taux', 'Taux'), ('mta', 'Montant')],
                                      required=True,
                                      default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                          'sn_sales.remise_methode', 'taux'))
    remise_applied_on = fields.Selection(string="Remise à appliquer",
                                         selection=[('article', 'Par article'), ('global', 'En global')],
                                         required=True,
                                         default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
                                             'sn_sales.remise_applied_on', 'global'))
    remise_valeur = fields.Float(string="Remise", store=True, readonly=True, compute='_amount_all',
                                 digits="montant")
    amount_ht_before_remise = fields.Float(string="Montant HT", store=True,
                                           readonly=True, compute='_amount_all' ,digits="montant" )

    ###########################################################################################################
    # Monetary
    amount_ht = fields.Float(string='Montant HT', store=True, readonly=True, compute='_amount_all',
                             track_visibility='onchange',
                             digits="montant",track_sequence=5)
    # Monetary
    amount_tva = fields.Float(string='TVA', store=True, readonly=True,
                              digits="montant", compute='_amount_all')
    # Monetary
    amount_ttc = fields.Float(string='Total TTC', store=True, readonly=True,
                              digits="montant", compute='_amount_all', track_visibility='always', track_sequence=6)

    # amount ttc sans les avances de paiement  (Rest à payer)
    amount_ttc_sec= fields.Float( string='Total TTC',compute='_amount_all',store=True, readonly=True, )

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sn_sales.commandes'))

    product_name_editable = fields.Boolean(string="Désignation éditable",  default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.product_name_editable')    )

    code_article_exist = fields.Boolean(string="Afficher Code article",  default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.code_article_exist') )

    special = fields.Boolean("Bon spécial")

    @api.depends('commande_lines')
    def _compute_lines_count(self):
        for rec in self:
            rec.commande_lines_count = len(rec.commande_lines)

    def action_confirm(self):
        qtys = sum(l.qty for l in self.commande_lines)
        if qtys <= 0 and not self.special:
            raise UserError(_('Les quantités sont nuls, Pas de confirmation '))
            return False
        else:
            self.update({
                'state': 'confirmed',
                'confirmation_date': fields.Date.today(),
            })
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


    def go2proforma(self):
        prfm_ref = self.env['sn_sales.proformas'].search_count([('id', '=', self.proforma_origin)])
        if prfm_ref > 0:
            form_view_id = self.env.ref('sn_sales.view_proforma_form').ids
            return {
                'views': [[form_view_id, 'form']],
                'name': _('Proforma'),
                'view_mode': 'form',
                'view_id': form_view_id,
                'res_model': 'sn_sales.proformas',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.proforma_origin
            }
        else:
            self.proforma_origin=0
            message = _('Proforma en relation non trouvée!.. Peut être supprimée.. Cette relation sera désormais déconnectée')
            title= _('Problème de liaison entre pièces')

            return self.env['sn_base.message_wizard'].message(title, message)

    def print_commande(self):
        return self.env.ref('sn_sales.action_report_commande').report_action(self)

    def write(self, vals):
        #vals['commande_lines'][0][2]['price_changed']
        if 'commande_lines' in vals.keys():
            for line in vals['commande_lines']:
                if not line[2]==False:
                    if line[0]==0: # adding new article while editing
                        if line[2]['price_changed']:
                           prod = self.env['sn_sales.product'].search( [('id', '=', line[2]['product_id'])] )
                           if prod:
                                if self.operation_type=='command':
                                    prod.update({'default_price':line[2]['price_unit']})
                                if self.operation_type=='purchase':
                                    prod.update({'purchase_price':line[2]['price_unit']})

                    if line[0]==1: # editing an article
                        if 'price_changed' in line[2].keys() and line[2]['price_changed']:
                            art_id=self.env['sn_sales.commande.lines'].search( [('id', '=', line[1])] ).product_id.id
                            prod = self.env['sn_sales.product'].search( [('id', '=', art_id)] )
                            if prod:
                                if self.operation_type=='command':
                                    prod.update({'default_price':line[2]['price_unit']})
                                if self.operation_type=='purchase':
                                    prod.update({'purchase_price':line[2]['price_unit']})

        return super(NticSaleCommande, self).write(vals)

    @api.model
    def create(self, vals):
        if 'commande_lines' in vals.keys():
            for line in vals['commande_lines']:
                if 'price_changed' in line[2].keys() and line[2]['price_changed']:
                    prod = self.env['sn_sales.product'].search( [('id', '=', line[2]['product_id'])] )
                    if prod:
                        if vals['operation_type']=='command':
                            prod.update({'default_price':line[2]['price_unit']})
                        if vals['operation_type']=='purchase':
                            prod.update({'purchase_price':line[2]['price_unit']})

        if vals.get('name')=='/':
            gwr = 'Sequencer'
            prefix='SQ/'
            if vals['operation_type']=='command':
                gwr = 'commande'
                prefix='BC/'
            if vals['operation_type']=='purchase':
                gwr = 'achat'
                prefix='ACH/'
            next_one=self.env['ir.sequence'].get(gwr)
            if not next_one:
                dict = {"prefix": prefix,
                        "code": gwr,
                        "name": gwr,
                        "active": True,
                        "padding": 4,
                        "implementation": "standard",
                        }
                self.env['ir.sequence'].create(dict)
                next_one=self.env['ir.sequence'].next_by_code(gwr)
            vals['name'] = next_one
            
        return super(NticSaleCommande, self).create(vals)
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################

class NticSaleCommandeLines(models.Model):
    _name = 'sn_sales.commande.lines'
    _description = 'Ntic commande Lines'
    _order = 'commande_id, sequence, id'

    @api.depends('price_unit', 'qty')
    def _haseb(self):
        for line in self:
            line.price_total=line.price_unit*line.qty

    commande_id = fields.Many2one('sn_sales.commandes', string='Commande Reference',
                                ondelete='cascade',
                               index=True,copy=False, readonly=True)
    company_id = fields.Many2one('res.company', 'Company', related='commande_id.company_id',store=True)

    name = fields.Text(string='Désignation', required=True)

    sequence = fields.Integer(string='Sequence', default=10)
    # recno = fields.Integer(string='N', )  

    price_unit = fields.Float('Prix Unit.', required=True,  default=0.0,
                              digits="montant",
                              track_visibility='onchange', track_sequence=8)
    price_list_libelle = fields.Char('Nom de liste de prix', default='')

    price_total = fields.Float(compute='_haseb', string='Total', digits="montant", default=0.0,  store=True)

    remise_taux = fields.Float(string='Remise %', digits="Remise Taux")
    remise_mta = fields.Float(string='Remise', digits="Remise Montant")

    product_id = fields.Many2one('sn_sales.product', string='Product',  change_default=True, ondelete='restrict') #,domain=[('sale_ok', '=', True)]

    productidid = fields.Integer(
        string='field_name',related='product_id.id'
    )

    product_code = fields.Char(string="Réf.", related='product_id.code' )
    product_categ_id = fields.Char(string="categorie", related='product_id.product_categ_id.name', store=True )

    # Qte Après calcule
    qty = fields.Float(string='Qte.', digits="Quantity", default=1.0 )

    product_image = fields.Binary('Product Image', related="product_id.image", store=False, readonly=False)

    user_id = fields.Many2one(related='commande_id.user_id', store=True, string='Vendeur', readonly=True)

    partner_id = fields.Many2one(related='commande_id.partner_id', store=True, string='Customer',    readonly=False)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note"),
        ('composed', "Composé")],  help="UX Raisons.")

    price_changed = fields.Boolean( string='Approbation du nouveau prix',store=False ,default= False   )
    price_touched = fields.Boolean( string='Prix modifié',store=False ,default= False   )

    operation_type = fields.Selection(string="Operation type", related='commande_id.operation_type',store=True )
    # _sql_constraints = [('commande_product_uniq',
    #                      'unique(product_id)',
    #                      'Duplicate products in order line not allowed !')]

    

    ##########################
    # overwitten in purchase #
    ##########################
    @api.onchange('product_id')
    def affect_name_to_designation(self):
        if not self.product_id.id:
            return

        price = 0
        libelle = ''
        if self.commande_id.tarification=='standard':
            price = self.product_id.default_price
            self.price_changed = False
            self.price_touched = False
        if self.commande_id.tarification == 'special':
            if self.commande_id.list_prix and self.product_id.pricelist_item_ids:
                for prix in self.product_id.pricelist_item_ids:
                    if prix.pricelist_id.id == self.commande_id.list_prix.id:
                        price = prix.fixed_price
                        libelle= prix.pricelist_id.name

        self.price_unit= price
        self.price_list_libelle=libelle
        self.name = self.product_id.name

  