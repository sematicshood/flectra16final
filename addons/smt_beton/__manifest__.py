# -*- coding: utf-8 -*-
{
    'name': "smt_beton",

    'summary': """
        Modul vertical untuk menangani pabrik cor beton di indonesia""",

    'description': """
        Modul in menangani mulai dari sales, produksi, delivery, sampai keuangan
    """,

    'author': "Sematics",
    'website': "http://sematics.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Vertical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'mrp','product','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/assets.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/stocks.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/marketing_dashboard.xml',
    ],
}