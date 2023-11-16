from odoo import models, fields, api

class SalesSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    command_confirmed_by_default = fields.Boolean("Commandes confirmées par défaut", config_parameter='sn_sales.command_confirmed_by_default')
    proforma_confirmed_by_default = fields.Boolean("Proformas confirmées par défaut", config_parameter='sn_sales.proforma_confirmed_by_default')
    display_recno = fields.Boolean("Afficher le numéros de lignes", config_parameter='sn_sales.display_recno')

    code_article_exist = fields.Boolean("Afficher des codes pour les articles", config_parameter='sn_sales.code_article_exist'  )

    # think to link promotions to group permission like group_promotions
    promotions_exist = fields.Boolean(string="Lancer des promotions", config_parameter='sn_sales.promotions_exist')
    validity_exist = fields.Boolean(string="Délais de validités exprimées en date", config_parameter='sn_sales.validity_exist')

    display_description = fields.Boolean("Afficher Déscription",config_parameter='sn_sales.display_description' )
    product_name_editable = fields.Boolean("Nom de produit modifiable",config_parameter='sn_sales.product_name_editable')
    using_logistics = fields.Boolean("Utiliser les logistics",config_parameter='sn_sales.using_logistics')
    using_codebare = fields.Boolean("Utiliser Code a barre",config_parameter='sn_sales.using_codebare')

    sequences = fields.Selection(string="Numérotation, bons de Vente", selection=[('global', 'Numérotation globale')], default='global',
                                    config_parameter='sn_sales.sequences')

    tva_exist = fields.Boolean("TVA Exist?", config_parameter='sn_sales.tva_exist')

    tva_taux = fields.Float(string="Taux (%)", config_parameter='sn_sales.tva_taux',default=19.0  )

    remise_exist = fields.Boolean(string="Remise Exist?", config_parameter='sn_sales.remise_exist' )

    remise_methode = fields.Selection(string="Methode de remise", config_parameter='sn_sales.remise_methode',
                    selection=[('taux', 'Taux'), ('mta', 'Montant')], required=True,
                    default='taux'    )

    remise_applied_on = fields.Selection(string="Methode d'application", config_parameter='sn_sales.remise_applied_on',
                selection=[('article', 'Par article'), ('global', 'En global')], required=True, default='global')

    remise_default_taux = fields.Float(string="Taux (%) par defaut", config_parameter='sn_sales.remise_default_taux', default=5.0  )
    remise_default_mta = fields.Float(string="Montant par defaut", config_parameter='sn_sales.remise_default_mta', default=100.0  )

    timbre_applicable = fields.Boolean(string="Timbre appliquable",config_parameter='sn_sales.timbre_applicable' )
    proforma_note_default = fields.Char(string='Proforma default Note', config_parameter='sn_sales.proforma_note_default',default='' )

    print_language = fields.Selection(string="Language d'impression", config_parameter='sn_sales.print_language',
                selection=[('user', 'Language User'), ('client', 'Language Client')], required=True, default='user')
