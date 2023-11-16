from odoo import models, fields, api, _

class NticPartner(models.Model):
    _name = 'sn_sales.partner'
    _description = 'Ntic Partner'
    _rec_name = 'display_name'

    # @api.depends('state_id')
    # def wich_region(self):
    #     for record in self:
    #         record.region = record.state_id.country_id.name

    def _lang_get(self):
        return self.env['res.lang'].get_installed()

    # def _get_categories(self):
    #     categs = []
    #     objet = 'client' # to be changed in other categories
    #     cats = self.env['sn_sales.taxonomies'].search([])
    #     for r in cats:
    #         if len(r.search([('name','=',objet)])):
    #             categs.append(r)

    #     return categs

    name = fields.Char(index=True, string="Nom", required=True)
    display_name = fields.Char(compute='_compute_display_name', store=True, index=True)
    ref = fields.Char(string="Code Client")

    lang = fields.Selection(_lang_get, string='Language', default=lambda self: self.env.lang)
    user_ids = fields.Many2many( "res.users", string= "Vendeurs", )

    website = fields.Char('Website Link')
    comment = fields.Text(string='Notes')
    active = fields.Boolean(default=True)
    address = fields.Char(string="Adresse")
    city = fields.Char()
    email = fields.Char()
    email_formatted = fields.Char(
        'Formatted Email', compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"')
    phone = fields.Char()
    mobile = fields.Char()

    function = fields.Char(string='Job Position')

    is_customer = fields.Integer(string='Is it Customer')  # default value goes with action
    is_supplier = fields.Integer(string='Is it Supplier',)

    tarification = fields.Selection(string="Tarification", selection=[
        ('standard', 'Standard'),
        ('special', 'Spécial') ],default='standard', required=True )
    list_prix = fields.Many2one("sn_sales.pricelist", string="Liste de prix")
    # TODO:: concerned field : to be deleted later
    concerned = fields.Char('Port-parole')    
    personne_ids = fields.One2many('sn_sales.personnes', 'partner_id', string="Personnages" )
    
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('sn_sales.partner'))

    categories_ids = fields.One2many('sn_sales.categories', 'partner_id', string='Categories',)


    wilaya_id = fields.Many2one("sn_base.wilayates", string='Wilaya', )
    commune_id = fields.Many2one("sn_base.communes", string='Commune', )
    region = fields.Char(string="Region",  store=False) #compute=wich_region,
    descript = fields.Char(string="Déscription")
    reg_com = fields.Char(string='Rég.Com', )
    art_imp = fields.Char(string="Art. Imp.", )
    mat_fisc = fields.Char(string="Mat. Fisc.",  )
    nis = fields.Char(string="N.I.S.",  )
    dept_limit = fields.Float(string="Max Amount",  required=False, )
    solvency = fields.Selection(string="Solvabilite",
                                selection=[('fidele', 'Fidèle'),
                                           ('solvable', 'Solvable'),
                                           ('non_solvable', 'Non Solvable'),
                                           ('bad_payed', 'Mal Payeur'),
                                           ],
                                required=False, default='solvable')
    image_variant_512 = fields.Image("Variant Image 512", max_width=512, max_height=512, store=True)
    image_variant_128 = fields.Image("Variant Image 128", related="image_variant_512", max_width=128, max_height=128,
                                     store=True)
    image_512 = fields.Image("Image 512", compute='_compute_image_512', inverse='_set_image_512')
    image = fields.Image("Image 128", compute='_compute_image')

    _sql_constraints = [
        ('code_partner_uniq', 'unique(ref)', "Code client doit être unique !"),
    ]

    def _set_image_512(self):
        for record in self:
            record.image_variant_512 = record.image_512

    def _compute_image_512(self):
        for record in self:
            record.image_512 = record.image_variant_512

    def _compute_image(self):
        for record in self:
            record.image = record.image_variant_128

    @api.depends('name')
    def _compute_display_name(self):
        for partner in self:
            partner.display_name = partner.name

        # diff = dict(show_address=None, show_address_only=None, show_email=None, html_format=None, show_vat=None)
        # names = dict(self.with_context(**diff).name_get())
        # for partner in self:
        #     partner.display_name = names.get(partner.id)

    @api.onchange('wilaya_id')
    def _get_communes(self):
        res = {}
        res['domain'] = {'commune_id': [('wilaya_id', '=', self.wilaya_id.id)]}
        self.commune_id= ''
        return res

    def client_commandes(self):
        tree_view_id = self.env.ref('sn_sales.view_orders_tree').ids
        return {
                'views': [[tree_view_id, 'tree']],
                'name': _('Commandes Client'),
                'view_mode': 'form',
                'view_id': tree_view_id,
                'res_model': 'sn_sales.commandes',
                'type': 'ir.actions.act_window',
                'domain': [("partner_id", '=', self.id)],
                'target': 'current',
             
            }