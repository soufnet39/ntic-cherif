# -*- coding: utf-8 -*-

{
    'name': 'nTIC Invoices',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3" , 
    'complexity': 'easy',
    'sequence': 1,
    'category': 'ntic',
    'description': "",
    'depends': ['sn_sales'],
    # depends on ntic base

    'summary': 'Invoices Created by Smail in  May 2019',
    'data': [

        'security/groups_rules.xml',
        'security/ir.model.access.csv',

        'report/styling.xml',
        'views/invoices.xml',
        'views/commande.xml',
        'views/partner.xml',

        'report/facture.xml',
        'report/etats_factures.xml',
        'report/reports.xml',
        #'report/etats_ventes.xml',
        
        'wizard/invoices.xml',
        'wizard/etat104.xml',
        
        'wizard/combine.xml',
        'views/res_config_settings_views.xml',

        'data/res_config.xml',

    ],
    'installable': True,
    'application': True,
}