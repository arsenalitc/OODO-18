from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestQuotationSubsections(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'consu',
            'list_price': 100.0,
        })
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })

    def test_create_section_and_subsection(self):
        """Test creating sections and subsections"""
        # Create a section
        section = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'display_type': 'line_section',
            'name': 'Hardware Section',
            'sequence': 10,
        })
        
        # Create a subsection
        subsection = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'display_type': 'line_subsection',
            'name': 'Servers Subsection',
            'parent_section_id': section.id,
            'sequence': 20,
        })
        
        self.assertEqual(subsection.parent_section_id, section)
        self.assertTrue(subsection.is_subsection)
        self.assertEqual(subsection.display_type, 'line_subsection')

    def test_subsection_total_calculation(self):
        """Test subsection total calculation"""
        # Create section
        section = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'display_type': 'line_section',
            'name': 'Hardware Section',
            'sequence': 10,
        })
        
        # Create subsection
        subsection = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'display_type': 'line_subsection',
            'name': 'Servers Subsection',
            'parent_section_id': section.id,
            'sequence': 20,
        })
        
        # Add product lines after subsection
        line1 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'name': 'Server 1',
            'product_uom_qty': 2,
            'price_unit': 1000.0,
            'sequence': 30,
        })
        
        line2 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'name': 'Server 2',
            'product_uom_qty': 1,
            'price_unit': 1500.0,
            'sequence': 40,
        })
        
        # Trigger computation
        subsection._compute_subsection_total()
        
        # Check total calculation (2*1000 + 1*1500 = 3500)
        expected_total = 2000.0 + 1500.0
        self.assertEqual(subsection.subsection_total, expected_total)

    def test_multiple_subsections(self):
        """Test multiple subsections under one section"""
        # Create section
        section = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'display_type': 'line_section',
            'name': 'Hardware Section',
            'sequence': 10,
        })
        
        # Create first subsection
        subsection1 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'display_type': 'line_subsection',
            'name': 'Servers Subsection',
            'parent_section_id': section.id,
            'sequence': 20,
        })
        
        # Add product under first subsection
        self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'name': 'Server',
            'product_uom_qty': 1,
            'price_unit': 1000.0,
            'sequence': 30,
        })
        
        # Create second subsection
        subsection2 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'display_type': 'line_subsection',
            'name': 'Networking Subsection',
            'parent_section_id': section.id,
            'sequence': 40,
        })
        
        # Add product under second subsection
        self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'name': 'Switch',
            'product_uom_qty': 2,
            'price_unit': 500.0,
            'sequence': 50,
        })
        
        # Both subsections should have the same parent section
        self.assertEqual(subsection1.parent_section_id, section)
        self.assertEqual(subsection2.parent_section_id, section)
        
        # Check that subsections are in the section's subsection_line_ids
        self.assertIn(subsection1, section.subsection_line_ids)
        self.assertIn(subsection2, section.subsection_line_ids)

    def test_subsection_without_section(self):
        """Test that subsections can be created without explicit parent section"""
        # Create a section first
        section = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'display_type': 'line_section',
            'name': 'Hardware Section',
            'sequence': 10,
        })
        
        # Create subsection - should auto-assign to last section
        subsection = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'display_type': 'line_subsection',
            'name': 'Auto-assigned Subsection',
            'sequence': 20,
        })
        
        # Should be automatically assigned to the section
        self.assertEqual(subsection.parent_section_id, section)
