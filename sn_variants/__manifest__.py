# -*- coding: utf-8 -*-

{
    'name': 'nTIC Products variants',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'http://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3",
    'complexity': 'easy',
    'sequence': 10,
    'category': 'nTIC',
    'description': "Unity Of Mesure Managment",
    'depends': ['sn_base', 'sn_sales'],

    'summary': 'Created by Smail in July 2020',
    'data': [
        'security/groups_rules.xml',
        'security/ir.model.access.csv',

        'views/styling.xml',
        
        'views/variants.xml',
        'views/products.xml',
        'views/commandes.xml',
        
        'views/res_config_settings_views.xml',

       
        

    ],
    'qweb': [

    ],

    'installable': True,
    'application': True,
}
