# -*- coding: utf-8 -*-

{
    'name': 'nTIC  Boxes',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3" ,
    'complexity': 'easy',
    'sequence': 5,
    'category': 'ntic',
    'description': "",
    'depends': ['sn_base','sn_sales','sn_purchases'],

    'summary': 'Boxes Created by Smail in  May 2019',
    'data': [

        'security/groups_rules.xml',
        'security/ir.model.access.csv',

       
        'views/boxes.xml',
        'views/operations.xml',
        'views/partner.xml',

        'views/commande.xml',

        'wizard/interboxes.xml',
        'wizard/etats_ventes.xml',

         'report/templates.xml',
         'report/reports.xml',
         'report/styling.xml',
         'report/commandes.xml',
         'report/etats_ventes.xml',
         'report/bon_caisse.xml',

        'views/res_config_settings_views.xml',
        'views/add_btns.xml',

        'data/res_config.xml'

    ],
    'demo': [    ],
    'qweb': ['static/src/xml/add_btns.xml'],
    'installable': True,
    'application': True,
}
