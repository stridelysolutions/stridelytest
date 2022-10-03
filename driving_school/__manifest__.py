# -*- coding: utf-8 -*-
{
    'name': "driving_school",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Driving School
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','hr','fleet','account','product','sale','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/wizard_login_view.xml',
        'wizard/wizard_invoice_view.xml',
        'wizard/wizard_students_view.xml',
        'views/views.xml',
        'wizard/wizard_report_classes_view.xml',
        'views/students.xml',
        'views/lessons.xml',
        'views/services.xml',
        'views/attendance.xml',
        'reports/report.xml',
        'reports/report_classes.xml',
        'reports/report_classes_html.xml',
        'views/cron.xml',
        'data/mail_template.xml',
    ],
    'license': 'LGPL-3',
}
