# -*- coding: utf-8 -*-
{
    'name': "mast_beauty_connector",

    'summary': """mast_beauty_connector""",

    'description': """mast_beauty_connector""",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '15.0.3',

    'depends': ['base','contacts','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
