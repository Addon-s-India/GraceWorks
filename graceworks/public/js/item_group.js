frappe.ui.form.on("Item Group", {
    onload: function (frm) {
        toggle_required(frm);
    },
    refresh: function (frm) {
        toggle_required(frm);
    },
});

function toggle_required(frm) {
    frm.toggle_reqd("item_group_name", true);
}
