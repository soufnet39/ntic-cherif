# -*- coding: utf-8 -*-
{
    'name': 'nTIC Base',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3",
    'complexity': 'easy',
    'sequence': 1,
    'category': 'ntic',
    'description': "",
    'depends': ['base',  'board',  'sms' ,'mail'],
 

    'summary': 'Created by Smail in April 2019',
    'data': [

        'security/groups_rules.xml',
        'security/ir.model.access.csv',

        'views/regions.xml',
        'views/communes.xml',
        'views/wilayates.xml',

        'views/menus.xml',
        'views/sequences.xml',

        'report/company_template.xml',

        'views/website_template.xml',
        'views/societes.xml',

        'views/res_config_settings_views.xml',
        'wizard/my_message.xml',

        'report/paper_format.xml',



        'data/rwc.xml',

    ],
    'demo': [

    ],
    'qweb': ['static/src/xml/template.xml'],


    'installable': True,
    'application': True,
}
