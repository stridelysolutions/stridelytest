# -*- coding: utf-8 -*-

{
    'name': "whatsapp_odoo",

    'summary': """
     Whats App Odoo""",

    'description': """
       Whats App Odoo
    """,
    'author': "Stridely Solutions",
    'website': "https://www.stridelysolutions.com/",
    'category': 'Technical',
    'version': '0.1',
    'depends': ['base','sale','account','stock','project'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/sale_portal_templates.xml',
        'views/sale_order_inherited.xml',
        'views/whatsapp_template.xml',
        'views/whatsapp_list.xml',
        'views/template_design.xml',
        'views/res_partner.xml',
        'wizard/wh_message_wizard.xml',
    ],
    
    'license': 'LGPL-3',
}
