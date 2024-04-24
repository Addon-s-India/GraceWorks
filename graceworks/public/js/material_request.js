frappe.ui.form.on("Material Request", {
    onload: function (frm) {
        toggle_required(frm);
    },
    refresh: function (frm) {
        toggle_required(frm);
    },
});

function toggle_required(frm) {
    frm.toggle_reqd("custom_project", true);
    frm.toggle_reqd("set_warehouse", true);
    frm.toggle_reqd("schedule_date", true);
    frm.toggle_reqd("custom_budget_code", true);
    frm.toggle_reqd("custom_site_indent_number", true);
    frm.toggle_reqd("custom_site_project_code", true);
    frm.toggle_reqd("custom_budget_amount", true);
}
