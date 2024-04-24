frappe.ui.form.on("Purchase Receipt", {
    onload: function (frm) {
        toggle_required(frm);
    },
    refresh: function (frm) {
        toggle_required(frm);
    },
});

function toggle_required(frm) {
    frm.toggle_reqd("project", true);
    frm.toggle_display("project", true);
    frm.toggle_reqd("cost_center", true);
    frm.toggle_display("cost_center", true);
    frm.toggle_reqd("supplier", true);
    frm.toggle_reqd("custom_material_received_date", true);
    frm.toggle_reqd("custom_bill_no", true);
    frm.toggle_reqd("custom_total_invoice_amount", true);
    frm.toggle_reqd("custom_challan_no", true);
    frm.toggle_reqd("custom_challan_date", true);
    frm.toggle_reqd("custom_bill_date", true);
}
