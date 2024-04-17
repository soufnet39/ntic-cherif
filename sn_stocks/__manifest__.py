# -*- coding: utf-8 -*-
{
    'name': 'nTIC  Stocks',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3" ,
    'complexity': 'easy',
    'sequence': 4,
    'category': 'ntic',
    'description': "",
    'depends': [ 'sn_base','sn_sales','sn_purchases'],
    # 'sn_sales'
    # depends on ntic base and ntic Sales

    'summary': 'Stocks Created by Smail in  May 2019',
    'data': [

        'security/groups_rules.xml',
        'security/ir.model.access.csv',

        'report/styling.xml',
        'views/stocks.xml',
        'views/commande.xml',
        'views/purchases.xml',
        'views/operations.xml',
        'views/products.xml',
        'views/etatstocks.xml',
        'views/eval_stocks.xml',

        'wizard/interstocks.xml',

        'report/operation.xml',
        'report/stocks.xml',
        'report/rest_stocks.xml',
        'report/reports.xml',
        'report/purchase.xml',

        'views/res_config_settings_views.xml',

        'views/add_btns.xml',
        'data/res_config.xml'

    ],
    'demo': [    ],
    'qweb': ['static/src/xml/add_btns.xml'],
    'installable': True,
    'application': True,
}

