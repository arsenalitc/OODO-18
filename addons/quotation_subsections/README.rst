====================
Quotation Subsections
====================

This module extends Odoo 18 Community Edition's quotation/sale order functionality to support subsections within sections, providing better organization and reporting capabilities.

Features
========

* Add subsections to sale order lines for better organization
* Automatic calculation of subsection-wise totals  
* Enhanced quotation reports with subsection grouping and totals
* Visual distinction between sections and subsections in forms and reports
* Parent-child relationship between sections and subsections

Installation
============

1. Copy this module to your Odoo addons directory
2. Update the addons list: ``./odoo-bin -u all -d your_database``
3. Install the module from Apps menu or via command line:
   ``./odoo-bin -i quotation_subsections -d your_database``

Usage
=====

Creating Sections and Subsections
----------------------------------

1. Open a quotation/sale order
2. In the order lines, click "Add a line"
3. Set the display type to:
   - **Section**: For main groupings
   - **Subsection**: For sub-groupings within sections
   - **Product**: For regular product lines

Organization Structure
----------------------

The recommended structure is:
- Section (e.g., "Hardware Components")
  - Subsection (e.g., "Servers")
    - Product lines
    - Product lines
  - Subsection (e.g., "Networking")
    - Product lines
    - Product lines

Features in Detail
==================

Subsection Totals
------------------

* Subsections automatically calculate totals for all product lines that follow them
* Totals are displayed in both the form view and printed reports
* Calculations update automatically when line items change

Visual Styling
--------------

* Sections have green left borders and light gray backgrounds
* Subsections have blue left borders and lighter gray backgrounds  
* Subsections are indented in reports for clear hierarchy

Report Enhancement
------------------

The quotation report now shows:
* Clear section headers
* Indented subsection headers with totals
* Proper grouping of products under their subsections
* Enhanced visual formatting

Technical Details
=================

Database Changes
----------------

* Extends ``sale.order.line`` model
* Adds ``display_type`` option: ``line_subsection``
* Adds ``parent_section_id`` field for section relationships
* Adds ``subsection_total`` computed field

Files Structure
---------------

::

    quotation_subsections/
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    │   ├── __init__.py
    │   └── sale_order_line.py
    ├── views/
    │   └── sale_order_views.xml
    ├── reports/
    │   └── sale_order_report.xml
    ├── security/
    │   └── ir.model.access.csv
    ├── static/
    │   ├── src/
    │   │   ├── css/
    │   │   │   └── subsection_styles.css
    │   │   ├── js/
    │   │   │   └── sale_order_subsections.js
    │   │   └── xml/
    │   │       └── subsection_templates.xml
    ├── demo/
    │   └── sale_order_demo.xml
    └── README.rst

Demo Data
=========

The module includes demo data showing a sample quotation with:
* Hardware Components section
  * Servers subsection (with server products)
  * Networking subsection (with network equipment)
* Software Licenses section  
  * Operating Systems subsection (with OS licenses)

Compatibility
=============

* Odoo 18.0 Community Edition
* Depends on: ``sale``, ``sale_management``

Support
=======

For issues or feature requests, please contact your Odoo implementation partner.

Credits
=======

* Author: Your Company
* Maintainer: Your Company
