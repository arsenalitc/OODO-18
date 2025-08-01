# Installation Guide - Quotation Subsections Module

## Prerequisites
- Odoo 18.0 Community Edition
- `sale` and `sale_management` modules must be installed

## Installation Steps

### 1. Module Installation
```bash
# Copy the module to your Odoo addons directory
cp -r quotation_subsections /path/to/odoo/addons/

# OR add the path to your odoo.conf file
addons_path = /path/to/your/addons,/path/to/quotation_subsections

# Install the module
./odoo-bin -i quotation_subsections -d your_database_name
```

### 2. Module Activation
1. Login to Odoo as Administrator
2. Go to Apps menu
3. Remove "Apps" filter and search for "Quotation Subsections"
4. Click Install

### 3. Verification
1. Go to Sales → Quotations
2. Create a new quotation
3. In Order Lines, you should see "Subsection" option in the display type dropdown
4. Create a section, then a subsection, then add products

## Usage Example

```
Hardware Components (Section)
├── Servers (Subsection) - Total: $13,500.00
│   ├── Dell PowerEdge Server (Qty: 2, Price: $5,000) = $10,000.00
│   └── HP ProLiant Server (Qty: 1, Price: $3,500) = $3,500.00
└── Networking Equipment (Subsection) - Total: $3,600.00
    ├── Cisco 48-Port Switch (Qty: 3, Price: $800) = $2,400.00
    └── Enterprise Router (Qty: 1, Price: $1,200) = $1,200.00

Software Licenses (Section)
└── Operating Systems (Subsection) - Total: $2,500.00
    └── Windows Server License (Qty: 5, Price: $500) = $2,500.00
```

## Features Enabled

✅ **Subsection Display Type**: New option in sale order lines  
✅ **Parent-Child Relationships**: Subsections linked to sections  
✅ **Automatic Totals**: Subsection totals calculated automatically  
✅ **Enhanced Reports**: Quotation PDFs show subsection totals  
✅ **Visual Styling**: Different colors for sections vs subsections  
✅ **Demo Data**: Sample quotation with subsections included  

## Testing

Run the included tests to verify functionality:
```bash
./odoo-bin -i quotation_subsections --test-enable -d your_database_name
```

## Troubleshooting

### Module Not Appearing
- Ensure the module is in the correct addons path
- Update apps list: Settings → Apps → Update Apps List

### Display Type Not Showing
- Refresh the browser
- Check that `sale_management` module is installed
- Verify user has Sales/User rights

### Totals Not Calculating
- Ensure products have prices set
- Check that product lines are placed after subsection lines
- Verify the sequence numbers are correct

## Support

For technical support, refer to the README.rst file or contact your Odoo implementation partner.
