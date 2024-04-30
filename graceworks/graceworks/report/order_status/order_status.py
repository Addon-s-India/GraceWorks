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
    
    if filters.get("from_date_po"):
        conditions += f" AND po.transaction_date >= '{filters.get('from_date_po')}'"
    if filters.get("to_date_po"):
        conditions += f" AND po.transaction_date <= '{filters.get('to_date_po')}'"
    if filters.get("supplier"):
        conditions += f" AND po.supplier = '{filters.get('supplier')}'"
    if filters.get("project"):
        conditions += f" AND po_item.project = '{filters.get('project')}'"
    if filters.get("company"):
        conditions += f" AND po.company = '{filters.get('company')}'"
    if filters.get("from_date_receipt"):
        conditions += f" AND receipt.posting_date >= '{filters.get('from_date_receipt')}'"
    if filters.get("to_date_receipt"):
        conditions += f" AND receipt.posting_date <= '{filters.get('to_date_receipt')}'"
    if filters.get("po_status"):
        conditions += f" AND po.status = '{filters.get('po_status')}'"
    if filters.get("receipt_status"):
        conditions += f" AND receipt.status = '{filters.get('receipt_status')}'"
    return conditions


def get_columns(filters):
    columns = [
        {
            "label": _("PO No"),
            "fieldname": "po_name",
            "fieldtype": "Link",
            "options": "Purchase Order",
            "width": 400
        },
        {
            "label": _("PO Date"),
            "fieldname": "po_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Supplier Name"),
            "fieldname": "supplier_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 150
        },
        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 200
        },
        {
            "label": _("Description"),
            "fieldname": "description",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("UOM"),
            "fieldname": "uom",
            "fieldtype": "Link",
            "options": "UOM",
            "width": 70
        },
        {
            "label": _("Ordered Qty"),
            "fieldname": "ordered_qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Due Date of Delivery"),
            "fieldname": "due_date_of_delivery",
            "fieldtype": "Date",
            "width": 130
        },
        {
            "label": _("PO Value (Net Total)"),
            "fieldname": "po_value_net_total",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Tax Amount"),
            "fieldname": "tax_amount",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("PO Value (Grand Total)"),
            "fieldname": "po_value_grand_total",
            "fieldtype": "Currency",
            "width": 140
        },
        # {
        #     "label": _("Qty Delivered"),
        #     "fieldname": "qty_delivered",
        #     "fieldtype": "Float",
        #     "width": 100
        # },
        {
            "label": _("Delivery Status"),
            "fieldname": "delivery_status",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("PO Delivery Days"),
            "fieldname": "po_delivery_days",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("GRN No"),
            "fieldname": "grn_no",
            "fieldtype": "Link",
            "options": "Purchase Receipt",
            "width": 400
        },
        {
            "label": _("GRN Date"),
            "fieldname": "grn_date",
            "fieldtype": "Date",
            "width": 130
        },
        {
            "label": _("Qty Received"),
            "fieldname": "qty_received",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Total Qty Received in PO"),
            "fieldname": "total_received_qty_in_po",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Qty Balance To Receive"),
            "fieldname": "qty_balance_to_receive",
            "fieldtype": "Float",
            "width": 140
        },
        {
            "label": _("Balance Purchase Invoice Qty"),
            "fieldname": "balance_purchase_invoice_qty",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": _("Purchase Invoice Value"),
            "fieldname": "balance_purchase_invoice_value",
            "fieldtype": "Currency",
            "width": 150
        }
    ]
    
    return columns


def get_data(filters):
    data = []
    
    conditions = get_conditions(filters)
    
    item_data = frappe.db.sql(f"""
                select
                    po.name as po_name,
                    po.transaction_date as po_date,
                    po.supplier_name as supplier_name,
                    po_item.item_group as item_group,
                    po_item.item_code as item_code,
                    po_item.description as description,
                    po_item.uom as uom,
                    po_item.qty as ordered_qty,
                    po_item.schedule_date as due_date_of_delivery,
                    po_item.base_net_amount as po_value_net_total,
                    po.custom_delivery_period as po_delivery_days,
                    (COALESCE(po_item.cgst_amount, 0) + COALESCE(po_item.sgst_amount, 0)) as tax_amount,
                    (po_item.base_net_amount + COALESCE(po_item.cgst_amount, 0) + COALESCE(po_item.sgst_amount, 0)) as po_value_grand_total,
                    po.status as delivery_status,
                    receipt.name as grn_no,
                    receipt.posting_date as grn_date,
                    receipt_item.received_qty as qty_received,
                    (po_item.qty - (
                        select sum(received_qty) 
                        from `tabPurchase Receipt Item` 
                        where 
                            purchase_order = po.name 
                            and parent in (
                                select name 
                                from `tabPurchase Receipt` 
                                where 
                                    docstatus = 1 
                                    and posting_date <= receipt.posting_date
                                    and posting_time <= receipt.posting_time
                            )
                    )) as qty_balance_to_receive,
                    (select sum(received_qty) 
                        from `tabPurchase Receipt Item` 
                        where 
                            purchase_order = po.name 
                            and parent in (
                                select name 
                                from `tabPurchase Receipt` 
                                where 
                                    docstatus = 1 
                                    and posting_date <= receipt.posting_date
                                    and posting_time <= receipt.posting_time
                            )
                    ) as total_received_qty_in_po,
                    receipt_item.custom_invoice_quantity as balance_purchase_invoice_qty,
                    receipt.custom_total_invoice_amount as balance_purchase_invoice_value
                from
                    `tabPurchase Order` po
                    left outer join `tabPurchase Order Item` po_item on po.name = po_item.parent
                    left outer join `tabPurchase Receipt Item` receipt_item on po.name = receipt_item.purchase_order
                    left outer join `tabPurchase Receipt` receipt on receipt_item.parent = receipt.name
                where
                    po.docstatus = 1
                    {conditions}
                """, as_dict=1)

    
    return item_data


    
    return item_data


