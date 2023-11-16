# -*- coding: utf-8 -*-

{
    'name': 'nTIC Sales',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3",
    'complexity': 'easy',
    'sequence': 0,
    'category': 'ntic',
    'description': "",
    'depends': ['sn_base', ],
    ## depends on ntic base + products
    # snailmail_account to send invoices or any documents by post

    'summary': 'Sales Created by Smail in May 2019',
    'data': [

        'security/groups_rules.xml',
        'security/ir.model.access.csv',

        'views/commande.xml',
        'views/partner.xml',
        'views/products.xml',
        'views/taxonomies.xml',
        'views/proforma.xml',
        'views/modes.xml',
        
        'views/product_categories.xml',

        'views/timbres.xml',

        'views/pricelist.xml',
        'views/template.xml',

        'report/templates.xml',
        'report/proforma.xml',
        'report/commande.xml',
        'report/reports.xml',
        'report/styling.xml',

        'wizard/etats_ventes.xml',
        # 'wizard/unify_clients.xml',
        'report/etats_ventes.xml',

        'views/res_config_settings_views.xml',
        'data/contents.xml',
        'data/modes.xml',
        'data/sales_data.xml',
        'data/pricelist.xml',
        'data/sales_data.xml',
        'data/res_config.xml',

    ],
    'demo': [
        # 'demo/ModuleName_demo.xml'
     

    ],

    'installable': True,
    'application': True,
}
