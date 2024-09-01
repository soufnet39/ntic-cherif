# -*- coding: utf-8 -*-
{
    'name': 'nTIC Cherif',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3" , 
    'complexity': 'easy',
    'sequence': 10,
    'category': 'nTIC',
    'description': "",
    'depends': ['sn_base', 'sn_sales' ,'sn_credit','sn_purchases' ],

    'summary': 'Gestion Commercial Created by Smail in Nov 2023',
    'data': [
        'security/groups_rules.xml',
        'security/ir.model.access.csv',
        'views/products.xml',
        'views/menus.xml',
        'views/commandes.xml',
        'views/partner.xml',
        'views/pricelist.xml',
        'views/purchases.xml',
        'views/black_list.xml',
        'views/etatstocks.xml',

        'report/commandes.xml',
        'report/header.xml',
        'report/products.xml',
        'report/reports.xml',
        'report/purchase.xml',
        'report/etats_ventes.xml',
        'report/etats_achats.xml',

        'wizard/change_state.xml',
        'wizard/print_prices.xml',
        'wizard/etats_ventes.xml',
        'wizard/etats_achats.xml',
        'data/scheduler.xml',
        'report/footer.xml'
    ],
    'qweb': [],

    'installable': True,
    'application': True,
}