# -*- coding: utf-8 -*-

{
    'name': 'nTIC Credit',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3" ,
    'complexity': 'easy',
    'sequence': 1,
    'category': 'ntic',
    'description': "",
    'depends': ['sn_base', 'sn_sales','sn_boxes', 'report_xlsx' ],
    ## depends on ntic base + ntic sale

    'summary': 'Gestion Commercial by Smail in May 2019',
    'data': [


        'security/groups_rules.xml',
        'security/ir.model.access.csv',

        'report/styling.xml',
        'report/prelevements.xml',
        'report/cuts.xml',
        'report/aksats.xml',
        'report/engagement.xml',
        'report/reports.xml',
        'report/commandes.xml',
        'report/retards.xml',

        'views/contrats.xml',
        #'views/aksats.xml',
        'views/prelevements.xml',
        'views/cuts.xml',
        'views/wilayates.xml',
        'views/centres.xml',
        'views/commande.xml',
        'views/partner.xml',

        "views/aksats_months.xml",
        "views/aksats_months_reel.xml",
        "views/products_rest.xml",

        'views/res_config_settings_views.xml',

        'wizard/system_errors.xml',
        'wizard/retards.xml'

    ],
    'demo': [

    ],
    #'js': ['static/src/js/widget_radio.js'],
    'qweb': ['static/src/xml/add_btns.xml'],

    'installable': True,
    'application': True,
}
