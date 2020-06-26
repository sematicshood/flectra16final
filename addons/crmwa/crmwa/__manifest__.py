# -*- coding: utf-8 -*-
{
    'name': "Crmwa",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Module CRMWA digunakan untuk melakukan kirim Whatsapp secara custome individu atau banyak nomor.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizards/send_wa_report.xml',
        'wizards/get_konsumen_data.xml',
        'menu.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/input_form.xml',
        'views/accounts_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}