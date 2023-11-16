# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'nTIC  Employees',
    'version': '1.1',
    'category': 'Human Resources',
    'sequence': 3,
    'summary': 'Centralize employee information',
    'description': "",
    'author': 'Moussaoui Smail',
    'website': 'https://www.soufnet.com',
    'support': 'info@soufnet.com',
    'images': [
        'images/hr_department.jpeg',
        'images/hr_employee.jpeg',
        'static/src/img/default_image.png',
    ],
    'depends': [
        'base_setup',
        'resource',
        'web',
    ],
    'data': [
        'security/hr_security.xml',
        'security/ir.model.access.csv',
        'views/hr_views.xml',
        'views/hr_templates.xml',
        'views/res_config_settings_views.xml',
        'views/mail_channel_views.xml',
        'data/hr_data.xml',
    ],
    'demo': [
       #  'data/hr_demo.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
