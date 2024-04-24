// Copyright (c) 2024, Addon-s India and contributors
// For license information, please see license.txt

frappe.query_reports["Indent MIS"] = {
    filters: [
        {
            fieldname: "from_indent_date",
            label: __("From Indent Date"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.add_months(
                frappe.datetime.get_today(),
                -1
            ),
        },
        {
            fieldname: "to_indent_date",
            label: __("To Indent Date"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.get_today(),
        },
        {
            fieldname: "from_po_date",
            label: __("From PO Date"),
            fieldtype: "Date",
        },
        {
            fieldname: "to_po_date",
            label: __("To PO Date"),
            fieldtype: "Date",
        },
        {
            fieldname: "supplier",
            label: __("Supplier"),
            fieldtype: "Link",
            options: "Supplier",
        },
        {
            fieldname: "budget_code",
            label: __("Budget Code"),
            fieldtype: "Link",
            options: "Budget Master",
        },
        {
            fieldname: "indent_status",
            label: __("Indent Status"),
            fieldtype: "Select",
            options: [
                "",
                "Draft",
                "Submitted",
                "Stopped",
                "Cancelled",
                "Pending",
                "Partially Ordered",
                "Partially Received",
                "Ordered",
                "Issued",
                "Transferred",
                "Received",
            ],
        },
        {
            fieldname: "po_status",
            label: __("PO Status"),
            fieldtype: "Select",
            options: [
                "",
                "Draft",
                "On Hold",
                "To Receive and Bill",
                "To Bill",
                "To Receive",
                "Completed",
                "Cancelled",
                "Closed",
                "Delivered",
            ],
        },
        {
            fieldname: "project",
            label: __("Project"),
            fieldtype: "Link",
            options: "Project",
        },
    ],
};
