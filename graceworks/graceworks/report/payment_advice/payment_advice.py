# Copyright (c) 2024, Addon-s India and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import logger

logger.set_log_level("DEBUG")
logger = frappe.logger("GraceWorks", allow_site=True, file_count=1)


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_conditions(filters):
    conditions = ""
    
    if filters.get("from_date"):
        conditions += f" AND pr.transaction_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND pr.transaction_date <= '{filters.get('to_date')}'"
    if filters.get("supplier"):
        conditions += f" AND pr.party = '{filters.get('supplier')}'"
    if filters.get("project"):
        conditions += f" AND pr.project = '{filters.get('project')}'"
    if filters.get("po_name"):
        conditions += f" AND pr.reference_name = '{filters.get('po_name')}'"
        
    return conditions
        


def get_columns(filters):
    columns = [
        {
            "label": _("Advance Request No"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Payment Request",
            "width": 240
        },
        {
            "label": _("Advance Request Date"),
            "fieldname": "transaction_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Project Code"),
            "fieldname": "project",
            "fieldtype": "Link",
            "options": "Project",
            "width": 150
        },
        {
            "label": _("Vendor Name"),
            "fieldname": "party_name",
            "fieldtype": "Data",
            "width": 230
        },
        {
            "label": _("PO No"),
            "fieldname": "reference_name",
            "fieldtype": "Link",
            "options": "Purchase Order",
            "width": 450
        },
        {
            "label": _("PO Date"),
            "fieldname": "po_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("PO Amount"),
            "fieldname": "po_amount",
            "fieldtype": "Currency",
            "width": 150 
        },
        {
            "label": _("Advance Paid"),
            "fieldname": "advance_paid",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Advance Requested Amount"),
            "fieldname": "advance_requested_amount",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Advance Requested Date"),
            "fieldname": "advance_requested_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": _("Advance Payment Date"),
            "fieldname": "advance_payment_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": _("Balance Amount"),
            "fieldname": "balance_amount",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Percentage/Lumpsum"),
            "fieldname": "percentage_lumpsum",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Approved"),
            "fieldname": "approved_amount",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("Paid"),
            "fieldname": "paid_amount",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("Balance"),
            "fieldname": "balance",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("Payment Delay in Days"),
            "fieldname": "payment_delay_in_days",
            "fieldtype": "Int",
            "width": 150
        }
    ]
    
    return columns


def get_data(filters):
    data = []
    
    condition = get_conditions(filters)
    
    advance_requests = frappe.db.sql(f"""
                            select
                                pr.name,
                                pr.transaction_date,
                                pr.project,
                                su.supplier_name as party_name,
                                pr.reference_name,
                                po.transaction_date as po_date,
                                po.grand_total as po_amount,
                                pe.paid_amount as advance_paid,
                                pr.grand_total as advance_requested_amount,
                                pr.transaction_date as advance_requested_date,
                                pe.posting_date as advance_payment_date,
                                pr.custom_amount_pending as balance_amount,
                                pr.grand_total as approved_amount,
                                pe.paid_amount as paid_amount,
                                (pr.grand_total - pe.paid_amount) as balance,
                                (pr.transaction_date - pe.posting_date) as payment_delay_in_days
                            from
                                `tabPayment Request` pr
                            left join
                                `tabPurchase Order` po on pr.reference_name = po.name
                            left join
                                `tabSupplier` su on pr.party = su.name
                            left join
                                `tabPayment Entry Reference` per on po.name = per.reference_name
                            left join
                                `tabPayment Entry` pe on per.parent = pe.name
                            where
                                pr.docstatus = 1
                                and pe.docstatus = 1
                                {condition}
                            """, as_dict=1)
                                
    return advance_requests


