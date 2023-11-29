# -*- coding: utf-8 -*-
{
    'name': 'nTIC Cherif Suppliers',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3" , 
    'complexity': 'easy',
    'sequence': 10,
    'category': 'nTIC',
    'description': "",
    'depends': ['sn_base', 'sn_sales' ,'sn_credit','sn_purchases','cherif'],

    'summary': 'Administration des fournisseurs Created by Smail in Nov 2023',
    'data': [
        'security/groups_rules.xml',
        'security/ir.model.access.csv',

        'views/suppliers.xml',
        'wizard/recap.xml',

        'wizard/add_btn.xml',
      

    ],
    'qweb': ['static/src/xml/add_btn.xml'],
    'installable': True,
    'application': True,
}