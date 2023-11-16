# -*- coding: utf-8 -*-

{
    'name': 'nTIC U.O.M',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'http://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3",
    'complexity': 'easy',
    'sequence': 10,
    'category': 'nTIC',
    'description': "Unity Of Mesure Managment",
    'depends': ['sn_base', 'sn_sales','sn_purchases','sn_invoices'],

    'summary': 'Gestion Commercial Created by Smail in May 2019',
    'data': [
        'security/groups_rules.xml',
        'security/ir.model.access.csv',

        'views/uom_categories.xml',
        'views/uom.xml',
        'views/products.xml',
        'views/proformas.xml',
        'views/commandes.xml',
        'views/invoices.xml',
        'views/purchases.xml',
        'views/res_config_settings_views.xml',

        'report/proformas.xml',
        'report/commandes.xml',
        'report/invoices.xml',
        'report/purchases.xml',

        'data/uom_categories.xml',
        'data/uom.xml'

    ],
    'qweb': [

    ],

    'installable': True,
    'application': True,
}
