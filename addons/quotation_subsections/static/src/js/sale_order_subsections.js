/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";

// Enhance the sale order line list view to better handle subsections
patch(ListController.prototype, "quotation_subsections.SaleOrderLineController", {
    
    /**
     * Override to add custom styling for subsections
     */
    setup() {
        this._super(...arguments);
        if (this.props.resModel === 'sale.order.line') {
            this.addSubsectionStyling();
        }
    },

    /**
     * Add custom styling for subsection rows
     */
    addSubsectionStyling() {
        // This will be called after the view is rendered
        this.env.bus.addEventListener('DOM_updated', () => {
            const rows = document.querySelectorAll('.o_list_view tbody tr');
            rows.forEach(row => {
                const displayTypeCell = row.querySelector('[name="display_type"]');
                if (displayTypeCell) {
                    const displayType = displayTypeCell.textContent.trim();
                    if (displayType === 'Subsection') {
                        row.classList.add('o_subsection_row');
                        row.style.backgroundColor = '#f8f9fa';
                        row.style.borderLeft = '3px solid #007bff';
                        row.style.fontWeight = 'bold';
                    } else if (displayType === 'Section') {
                        row.classList.add('o_section_row');
                        row.style.backgroundColor = '#e9ecef';
                        row.style.borderLeft = '4px solid #28a745';
                        row.style.fontWeight = 'bold';
                    }
                }
            });
        });
    },

    /**
     * Custom logic for adding new subsections
     */
    async onAddSubsection() {
        const context = {
            default_display_type: 'line_subsection',
            default_order_id: this.props.context.default_order_id,
        };
        
        return this.model.orm.create('sale.order.line', [{
            display_type: 'line_subsection',
            name: 'New Subsection',
            order_id: this.props.context.default_order_id,
        }], { context });
    }
});

// Register custom field widget for subsection totals
import { Component } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class SubsectionTotalField extends Component {
    static template = "quotation_subsections.SubsectionTotalField";
    static props = {
        ...standardFieldProps,
    };

    get formattedValue() {
        if (this.props.value) {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD'
            }).format(this.props.value);
        }
        return '$0.00';
    }
}

registry.category("fields").add("subsection_total", SubsectionTotalField);
