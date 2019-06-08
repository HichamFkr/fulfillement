# -*- coding: utf-8 -*-
{
    'name': "insidjam_stock_fulfillement",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'product',
                'sale',
                'sale_order_type',
                'insidjam_pack_std',
                'web','web_list_html_widget'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/eligibilite.xml',
        'views/partner_sla.xml',
        'views/line_eligible.xml',
        'views/assets.xml',
        'data/service_rules_level.xml',
        'views/sla_tooltip.xml',
        'wizard/confirm_line_fulfill.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}