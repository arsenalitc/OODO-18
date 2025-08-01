{
    'name': 'Quotation Subsections',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Add subsections functionality to quotations/sale orders',
    'description': """
        This module extends the quotation/sale order functionality to support subsections within sections.
        Features:
        - Add subsections to sale order lines
        - Organize quotation lines with sections and subsections
        - Calculate subsection-wise totals in quotation output
        - Enhanced quotation report with subsection grouping
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['sale', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'reports/sale_order_report.xml',
    ],
    'demo': [
        'demo/sale_order_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'quotation_subsections/static/src/css/subsection_styles.css',
            'quotation_subsections/static/src/js/sale_order_subsections.js',
            'quotation_subsections/static/src/xml/subsection_templates.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
