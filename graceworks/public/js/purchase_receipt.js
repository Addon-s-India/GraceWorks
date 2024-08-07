frappe.ui.form.on('Purchase Receipt', {
    onload: function(frm) {
        toggle_required(frm);
        fetch_order_qty_and_copy_balance(frm);
        set_read_only_fields(frm);
    },
    refresh: function(frm) {
        toggle_required(frm);
        fetch_order_qty_and_copy_balance(frm);
        set_read_only_fields(frm);
    }
});

function toggle_required(frm) {
    frm.toggle_reqd("set_warehouse", true);
    frm.toggle_reqd("supplier", true);
    frm.toggle_reqd("custom_material_received_date", true);
    frm.toggle_reqd("custom_bill_no", true);
    frm.toggle_reqd("custom_total_invoice_amount", true);
    frm.toggle_reqd("custom_challan_no", true);
    frm.toggle_reqd("custom_challan_date", true);
    frm.toggle_reqd("custom_bill_date", true);
    frm.fields_dict.items.grid.toggle_reqd("project", true);
    frm.fields_dict.items.grid.toggle_reqd("warehouse", true);
}

function fetch_order_qty_and_copy_balance(frm) {
    frm.doc.items.forEach(item => {
        if (item.purchase_order && item.purchase_order_item) {
            frappe.call({
                method: 'graceworks.api.get_order_qty',
                args: {
                    purchase_order_item: item.purchase_order_item
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.model.set_value(item.doctype, item.name, 'custom_order_qty', r.message.qty);
                        frappe.model.set_value(item.doctype, item.name, 'custom_balance_qty', item.qty);
                        console.log(`Set custom_order_qty for ${item.item_code} to ${r.message.qty}`);
                        console.log(`Copied qty to custom_balance_qty for ${item.item_code} as ${item.qty}`);
                    }
                }
            });
        } else {
            frappe.model.set_value(item.doctype, item.name, 'custom_balance_qty', item.qty);
            console.log(`Copied qty to custom_balance_qty for ${item.item_code} as ${item.qty}`);
        }
    });
}

function set_read_only_fields(frm) {
    frm.fields_dict.items.grid.toggle_enable('custom_order_qty', false);
    frm.fields_dict.items.grid.toggle_enable('custom_balance_qty', false);
}
