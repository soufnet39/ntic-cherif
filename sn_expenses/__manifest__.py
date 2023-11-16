# -*- coding: utf-8 -*-

{
    'name': 'Ntic Expenses',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3" ,
    'complexity': 'easy',
    'sequence': 6,
    'category': 'Ntic',
    'description': "",
    'depends': ['sn_base','sn_boxes'],
    # depends on Ntic base and Ntic Boxes

    'summary': 'Expenses Created by Smail in  May 2019',
    'data': [

        'security/groups_rules.xml',
        'security/ir.model.access.csv',

        'report/styling.xml',
        'views/expenses.xml',
        'views/boxes.xml',
        'views/operations.xml',
        'views/res_config_settings_views.xml',

        'views/add_btns.xml',


    ],
    'demo': [

    ],
    'qweb': ['static/src/xml/add_btns.xml'],
    'installable': True,
    'application': True,
}
