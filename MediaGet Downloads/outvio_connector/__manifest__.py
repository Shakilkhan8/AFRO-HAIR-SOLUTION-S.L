# -*- coding: utf-8 -*-
{
    'name': 'Outvio Connector',
    'version': '15.0.0.3.0',
    'category': 'Inventory/Delivery',
    'license': 'OPL-1',
    'depends': ['delivery'],
    'summary': 'This module sends order details from Odoo to Outvio',
    'author': 'Outvio',
    'website': 'https://outvio.com',
    'images': ['static/description/cover.jpg'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/outvio_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': 'populate_api_url_hook',
    'uninstall_hook': 'clear_api_token_hook'
}
