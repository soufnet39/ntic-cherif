from odoo import models, fields, tools,api, _
#from odoo.exceptions import ValidationError, RedirectWarning, UserError


class NticProduct(models.Model):
    _name = "sn_sales.product"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _description = 'Ntic Product'
    #_rec_name = 'display_name'



    # def _get_default_uom_id(self):
    #     return self.env["sn_sales.uom"].search([], limit=1, order='id').id

    name = fields.Char('Name', required=True, translate=True)
    display_name = fields.Char(compute='_compute_display_name', store=True, index=True)

    code = fields.Char( 'Reference Interne', )
    active = fields.Boolean(  'Active', default=True, help="If unchecked, it will allow you to hide the product without removing it.")
    sequence = fields.Integer('Sequence', default=10000, help='Ordonner la liste de products')
    description = fields.Text(   'Description', translate=True)
    note = fields.Text('Note', translate=True)


    sale_ok = fields.Boolean('Peut être vendu', default=True)

    default_price = fields.Float('Prix de vente standard',
                                 digits="Product Price",
                                 groups="base.group_user", )

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)
    categories_ids = fields.One2many('sn_sales.categories', 'product_id', 'Categories',  ) #self.farz('product')
    product_commande_lines = fields.One2many('sn_sales.commande.lines', 'product_id')


    #### Unity of Mesure ##################################################################################################
    # TODO:: Make uom_exist always equals to self.env['ir.config_parameter'].sudo().get_param('sn_sales.uom_exist')
    #uom_exist = fields.Boolean(string="Unité de mesure Exist",compute='_get_all_variables' , default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.uom_exist')     )
    using_logistics = fields.Boolean(string="utiliser logistics",compute='_get_all_variables' , default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.using_logistics')     )
    using_codebare = fields.Boolean(string="Code a barre Exist",compute='_get_all_variables' , default=lambda self: self.env['ir.config_parameter'].sudo().get_param('sn_sales.using_codebare')     )

    #uom_sale_id = fields.Many2one('sn_sales.uom', 'Unité de Mesure Vente', default=_get_default_uom_id, required=True, help="Unité de mesure de vente par defaut.")
    #uom_name = fields.Char(string='Unité de Mesure', related='uom_sale_id.name', readonly=True)

    ###########################################################################################################

    sale_methode = fields.Selection(string="Methode de prix", selection=[('unified', 'Unifié sur prix standard'), ('list', 'Unifié ou Liste des prix'), ], default='unified', required=True )

    barcode = fields.Char('code a barre', copy=False)

    pricelist_item_ids = fields.One2many('sn_sales.pricelist.item', 'product_id', 'Pricelist Items')

    product_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service')], string='Product Type', default='consu', required=True,
        help='A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')

    image_variant_512 = fields.Image("Variant Image 512",  max_width=512, max_height=512, store=True)
    image_variant_128 = fields.Image("Variant Image 128", related="image_variant_512", max_width=128, max_height=128, store=True)
    image_512 = fields.Image("Image 512", compute='_compute_image_512',inverse='_set_image_512')
    image = fields.Image("Image 128", compute='_compute_image')

    
    product_categ_id = fields.Many2one(
        'sn_sales.products_categories',
        'Catégorie'      ,
        ondelete='restrict'  
        
    )
    

    def _set_image_512(self):
        for record in self:
            record.image_variant_512 = record.image_512

    def _compute_image_512(self):
        for record in self:
            record.image_512 = record.image_variant_512


    def _compute_image(self):
        for record in self:
            record.image = record.image_variant_128
   
    _sql_constraints = [
        ('barcode_uniq', 'unique(barcode)', "Chaque code a barre doit être assigne a un seul produit !"),
    ]

    @api.depends('name')
    def _compute_display_name(self):
        for art in self:
            art.display_name = art.name

    def _get_all_variables(self):
        #uom_exist = self.env["ir.config_parameter"].sudo().get_param("sn_sales.uom_exist")
        using_logistics = self.env["ir.config_parameter"].sudo().get_param("sn_sales.using_logistics")
        using_codebare = self.env["ir.config_parameter"].sudo().get_param("sn_sales.using_codebare")
        for record in self:
            #record.uom_exist = uom_exist
            record.using_logistics = using_logistics
            record.using_codebare = using_codebare
        # TODO:: can be replaced by
        #  record.update({
        #         "uom_exist" : uom_exist,
        #         "record.using_logistics" : using_logistics,
        #         "record.using_codebare" : using_codebare
        #     })

    def copy(self, default=None):
        if default is None:
            default = {}
        if 'name' not in default:
            default['name'] = _("%s (copy)") % self.name
        return super(NticProduct, self).copy(default=default)


