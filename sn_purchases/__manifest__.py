# -*- coding: utf-8 -*-

{
    'name': 'nTIC  Purchases',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3" ,
    'complexity': 'easy',
    'sequence': 1,
    'category': 'ntic',
    'description': "",
    'depends': ['sn_sales',],

    # depends on ntic base and ntic Sales

    'summary': 'Purchases Created by Smail in  May 2019',
    'data': [

        'security/groups_rules.xml',
        'security/ir.model.access.csv',

        'report/reports.xml',
        'report/purchase.xml',
        'report/etats_achats.xml',

        'report/styling.xml',
        'views/purchases.xml',
        #'views/charges.xml',
        'views/products.xml',
        #'views/supplier.xml',
        'views/partner.xml',

        'wizard/purchases.xml',


        'data/contents.xml',
        'views/res_config_settings_views.xml',
        'data/res_config.xml'
    ],
    'demo': [

    ],

    'installable': True,
    'application': True,
}
