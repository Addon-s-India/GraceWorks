frappe.ui.form.on("Stock Entry", {
    setup: function (frm) {
        frm.set_query("item_code", "items", function () {
            return {
                query: "graceworks.stock_entry.custom_item_query",
                filters: { from_warehouse: frm.doc.from_warehouse },
            };
        });
    },
    onload: function (frm) {
        toggle_required(frm);
        frm.toggle_reqd("from_warehouse", true);
        frm.set_query("item_code", "items", function () {
            return {
                query: "graceworks.stock_entry.custom_item_query",
                filters: { from_warehouse: frm.doc.from_warehouse },
            };
        });
        frm.set_query("stock_entry_type", function () {
            return {
                query: "graceworks.stock_entry.custom_stock_entry_type_query",
            };
        });
    },
    validate: function (frm) {
        if (!check_qty_items(frm)) {
            frappe.validated = false;
        }
    },
    refresh: function (frm) {
        toggle_required(frm);
    },
});

frappe.ui.form.on("Stock Entry Detail", {
    qty: function (frm, cdt, cdn) {
        // qty should not be greater then actual qty
        var d = locals[cdt][cdn];
        if (d.qty > d.actual_qty) {
            frappe.msgprint(
                "Quantity should not be greater than actual quantity - " +
                    d.actual_qty
            );
            frappe.model.set_value(cdt, cdn, "qty", d.actual_qty);
        }
    },
});

function check_qty_items(frm) {
    var items = frm.doc.items;
    var invalidRows = []; // Array to store the indices of invalid rows

    // Loop through each item in the items table
    for (var i = 0; i < items.length; i++) {
        if (items[i].qty > items[i].actual_qty) {
            // Push the row number (i + 1 for 1-based index) and the item code to the invalidRows array
            invalidRows.push(
                `<br> <b> Row ${i + 1} </b> (Item Code: ${
                    items[i].item_code
                }) Actual Qty: ${items[i].actual_qty}`
            );
        }
    }

    // Check if there are any invalid rows
    if (invalidRows.length > 0) {
        // Join all entries in invalidRows array into a single string separated by comma
        var msg = invalidRows.join(", ");
        // Display the message to the user
        frappe.msgprint(
            "Quantity should not be greater than actual quantity. Check:                          \n" +
                msg
        );
        return false; // Return false to indicate validation failure
    }
    return true; // Return true if all rows are valid
}

function toggle_required(frm) {
    frm.toggle_reqd("custom_issued_to", true);
    frm.toggle_reqd("company", true);
    frm.toggle_reqd("custom_request_number", true);
    frm.toggle_reqd("posting_date", true);
}
