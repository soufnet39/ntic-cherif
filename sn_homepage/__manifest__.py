{
    'name': 'nTIC home Page',
    'version': '1.0',
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'license': "AGPL-3" ,
    'complexity': 'easy',
    'sequence': 1,
    'category': 'ntic',
    'description': "",
    'depends': ['sn_base'],

    # depends on ntic base and ntic Sales

    'summary': 'Purchases Created by Smail in  May 2019',
    'data': [
        'security/ir.model.access.csv',
        'views/homepage.xml',


    ],
    'qweb': [
       "static/src/xml/homepage.xml",
    ],


    'installable': True,
    'application': True,
}