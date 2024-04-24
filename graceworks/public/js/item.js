frappe.ui.form.on("Item", {
    refresh: function (frm) {
        frm.toggle_reqd("item_name", true);
    },
    onload: function (frm) {
        frm.toggle_reqd("item_name", true);
    },
});
