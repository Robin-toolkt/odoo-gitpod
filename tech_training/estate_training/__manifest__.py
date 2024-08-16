# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
    A Basic Real Estate Module""",

    'description': """
Long description of module's purpose
    """,

    'author': "Toolkit",
    'website': "https://www.toolkt.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/property.xml',
        'views/property_type.xml',
        'views/property_tags.xml',
        'views/property_offer.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

