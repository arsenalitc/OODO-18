from odoo import models, fields, api
from odoo.tools.translate import _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    display_type = fields.Selection([
        ('line_section', 'Section'),
        ('line_note', 'Note'),
        ('line_subsection', 'Subsection'),
    ], string='Display Type', help="Technical field used to differentiate normal lines from sections, notes and subsections.")
    
    parent_section_id = fields.Many2one(
        'sale.order.line',
        string='Parent Section',
        domain="[('order_id', '=', order_id), ('display_type', '=', 'line_section')]",
        help="The parent section this subsection belongs to"
    )
    
    subsection_line_ids = fields.One2many(
        'sale.order.line',
        'parent_section_id',
        string='Subsection Lines',
        domain="[('display_type', '=', 'line_subsection')]"
    )
    
    is_subsection = fields.Boolean(
        string='Is Subsection',
        compute='_compute_is_subsection',
        store=True
    )
    
    subsection_total = fields.Monetary(
        string='Subsection Total',
        compute='_compute_subsection_total',
        store=True,
        currency_field='currency_id'
    )
    
    @api.depends('display_type')
    def _compute_is_subsection(self):
        for line in self:
            line.is_subsection = line.display_type == 'line_subsection'
    
    @api.depends('order_id.order_line.price_subtotal', 'order_id.order_line.parent_section_id')
    def _compute_subsection_total(self):
        for line in self:
            if line.display_type == 'line_subsection':
                # Get all product lines that come after this subsection and before next section/subsection
                order_lines = line.order_id.order_line.sorted('sequence')
                subsection_lines = []
                found_subsection = False
                
                for order_line in order_lines:
                    if order_line.id == line.id:
                        found_subsection = True
                        continue
                    
                    if found_subsection:
                        # Stop if we hit another section or subsection
                        if order_line.display_type in ['line_section', 'line_subsection']:
                            break
                        # Add product lines to our subsection
                        if not order_line.display_type:
                            subsection_lines.append(order_line)
                
                line.subsection_total = sum(subsection_lines.mapped('price_subtotal'))
            else:
                line.subsection_total = 0.0

    @api.model
    def create(self, vals):
        # Set parent section for subsections
        if vals.get('display_type') == 'line_subsection' and vals.get('order_id'):
            order = self.env['sale.order'].browse(vals['order_id'])
            # Find the last section in the order to set as parent
            last_section = order.order_line.filtered(
                lambda l: l.display_type == 'line_section'
            ).sorted('sequence', reverse=True)[:1]
            if last_section:
                vals['parent_section_id'] = last_section.id
        
        return super().create(vals)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.depends('order_line.price_subtotal', 'order_line.display_type')
    def _compute_subsection_totals(self):
        """Compute totals for each subsection in the order"""
        for order in self:
            subsections = order.order_line.filtered(lambda l: l.display_type == 'line_subsection')
            for subsection in subsections:
                subsection._compute_subsection_total()
