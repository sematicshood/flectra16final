# -*- coding: utf-8 -*-
{
    'name': "smt_gajian",

    'summary': """
        Perhitungan payroll dengan tambahan dari :
        1. Perhitungan insentif harian
        2. Perhitungan insentif dari gamification""",

    'description': """
        Update perhitungan payroll dengan penambahan fitur ambil dari  
        gamification, dan insentif harian
    """,

    'author': "Sematics",
    'website': "https://sematics.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','account','mail','web','simontir'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/penggajian.xml',
        'views/insentif.xml',
        'views/rekapgajinya.xml',
        'views/parinsentif.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}