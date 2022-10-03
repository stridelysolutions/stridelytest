# -*- coding: utf-8 -*-
{
    'name': "translate_tool",
    'summary': """translate_tool""",
    'description': """Translate Tool""",
    'author': "Stridely Solutions",
    'website': "https://www.stridelysolutions.com/",
    'category': 'Technical',
    'version': '15.0.0.1.0',
    'depends': ['base'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/translation_wizard_view.xml',
        'views/settings_menu.xml',
    ],
    'license': 'LGPL-3',
}
