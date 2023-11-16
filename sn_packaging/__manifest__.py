# -*- coding: utf-8 -*-

{
    'name': 'nTIC Packaging & Logistics',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'http://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3",
    'complexity': 'easy',
    'sequence': 10,
    'category': 'nTIC',
    'description': "Packagin an logistics",
    'depends': ['sn_base', 'sn_sales','sn_purchases','sn_invoices'],

    'summary': 'Gestion Commercial Created by Smail in May 2019',
    'data': [
        'security/groups_rules.xml',
        'security/ir.model.access.csv',


    ],
    'qweb': [

    ],

    'installable': True,
    'application': True,
}
