// Copyright (c) 2024, Addon-s India and contributors
// For license information, please see license.txt
// get from date from last month to today
frappe.query_reports["Payment Advice"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.add_months(
                frappe.datetime.get_today(),
                -1
            ),
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.get_today(),
        },
        {
            fieldname: "project",
            label: __("Project"),
            fieldtype: "Link",
            options: "Project",
        },
        {
            fieldname: "supplier",
            label: __("Vendor"),
            fieldtype: "Link",
            options: "Supplier",
        },
        {
            fieldname: "po_name",
            label: __("Purchase Order"),
            fieldtype: "Link",
            options: "Purchase Order",
        },
    ],
};
