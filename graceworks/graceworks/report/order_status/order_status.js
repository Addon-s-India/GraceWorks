// Copyright (c) 2024, Addon-s India and contributors
// For license information, please see license.txt

frappe.query_reports["Order Status"] = {
    filters: [
        {
            fieldname: "from_date_po",
            label: __("From Date (PO)"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.add_months(
                frappe.datetime.get_today(),
                -1
            ),
        },
        {
            fieldname: "to_date_po",
            label: __("To Date (PO)"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.get_today(),
        },
        {
            fieldname: "supplier",
            label: __("Vendor"),
            fieldtype: "Link",
            options: "Supplier",
        },
        {
            fieldname: "from_date_receipt",
            label: __("From Date (Receipt)"),
            fieldtype: "Date",
        },
        {
            fieldname: "to_date_receipt",
            label: __("To Date (Receipt)"),
            fieldtype: "Date",
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
            fieldname: "receipt_status",
            label: __("Purchase Receipt Status"),
            fieldtype: "Select",
            options: [
                "",
                "Draft",
                "To Bill",
                "Completed",
                "Return Issued",
                "Cancelled",
                "Closed",
            ],
        },
    ],
};
