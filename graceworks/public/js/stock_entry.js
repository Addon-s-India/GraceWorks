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
});
