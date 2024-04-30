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
    
    if filters.get("from_indent_date"):
        conditions += f" AND mr.transaction_date >= '{filters.get('from_indent_date')}'"
    if filters.get("to_indent_date"):
        conditions += f" AND mr.transaction_date <= '{filters.get('to_indent_date')}'"
    if filters.get("from_po_date"):
        conditions += f" AND po.transaction_date >= '{filters.get('from_po_date')}'"
    if filters.get("to_po_date"):
        conditions += f" AND po.transaction_date <= '{filters.get('to_indent_date')}'"
    if filters.get("supplier"):
        conditions += f" AND po.supplier = '{filters.get('supplier')}'"
    if filters.get("budget_code"):
        conditions += f" AND mr.custom_budget_code = '{filters.get('budget_code')}'"
    if filters.get("project"):
        conditions += f" AND mr.custom_project = '{filters.get('project')}'"
    if filters.get("indent_status"):
        conditions += f" AND mr.status = '{filters.get('indent_status')}'"
    if filters.get("po_status"):
        conditions += f" AND po.status = '{filters.get('po_status')}'"
        
    return conditions


def get_columns(filters):
    columns = [
        {
            "label": _("Indent No"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Payment Request",
            "width": 240
        },
        {
            "label": _("Indent Date"),
            "fieldname": "transaction_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "Item Group",
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 150
        },
        {
            "label": "Item Code",
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 250
        },
        {
            "label": "Item Name",
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 430
        },
        {
            "label": "Item Description",
            "fieldname": "item_description",
            "fieldtype": "Data",
            "width": 430
        },
        {
            "label": "UOM",
            "fieldname": "uom",
            "fieldtype": "Link",
            "options": "UOM",
            "width": 80
        },
        {
            "label": "Indent Qty",
            "fieldname": "indent_qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": "PO No",
            "fieldname": "po_name",
            "fieldtype": "Link",
            "options": "Purchase Order",
            "width": 450
        },
        {
            "label": "PO Date",
            "fieldname": "po_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "Deff. Indent & PO Date",
            "fieldname": "diff_indent_po_date",
            "fieldtype": "Int",
            "width": 150
        },
        {
            "label": "PO Qty",
            "fieldname": "po_qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": "PO Value (Net Total)",
            "fieldname": "po_net_total",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "PO Value (Grand Total)",
            "fieldname": "po_grand_total",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Tax Amount",
            "fieldname": "tax_amount",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Balance to Order",
            "fieldname": "balance_to_order",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": "Vendor Name",
            "fieldname": "party_name",
            "fieldtype": "Data",
            "width": 230
        },
        {
            "label": "Advance Request Date",
            "fieldname": "advance_requested_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": "Advance Approved",
            "fieldname": "advance_approved",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Advance Paid Date",
            "fieldname": "advance_paid_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": "Advance Paid",
            "fieldname": "advance_paid",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "PO Delivery Days",
            "fieldname": "po_delivery_days",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": "Delivery Status",
            "fieldname": "delivery_status",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Qty Received",
            "fieldname": "qty_received",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": "First Delivery Date",
            "fieldname": "first_delivery_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "Last Delivery Date",
            "fieldname": "last_delivery_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "Calc Delivery Days",
            "fieldname": "calc_delivery_days",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Qty Balance to Received",
            "fieldname": "qty_balance_to_received",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": "Remarks",
            "fieldname": "remarks",
            "fieldtype": "Data",
            "width": 230
        },
        {
            "label": "Indent Status",
            "fieldname": "indent_status",
            "fieldtype": "Data",
            "width": 140
        },
        {
            "label": "Budget Code",
            "fieldname": "budget_code",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Budget Amount",
            "fieldname": "budget_amount",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Site Indent No",
            "fieldname": "site_indent_no",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Balance Indent Qty",
            "fieldname": "balance_indent_qty",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": "Diff Indent Creation & Approval",
            "fieldname": "diff_indent_creation_approval",
            "fieldtype": "Int",
            "width": 150
        },
        {
            "label": "Diff Between Indent & PO",
            "fieldname": "diff_indent_po",
            "fieldtype": "Int",
            "width": 150
        },
        {
            "label": "Balance in Store",
            "fieldname": "balance_in_store",
            "fieldtype": "Float",
            "width": 150            
        },
        {
            "label": "Indent Closed",
            "fieldname": "indent_closed",
            "fieldtype": "Boolean",
            "width": 100
        },
        {
            "label": "PO Closed",
            "fieldname": "po_closed",
            "fieldtype": "Boolean",
            "width": 100
        },
        {
            "label": "Variance",
            "fieldname": "variance",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": "Purchase Invoice Qty",
            "fieldname": "purchase_invoice_qty",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": "Purchase Invoice Value",
            "fieldname": "purchase_invoice_value",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Balance Purchase Invoice Value",
            "fieldname": "balance_purchase_invoice_value",
            "fieldtype": "Float",
            "width": 150
        }
    ]
    
    return columns


def get_data(filters):
    
    condition = get_conditions(filters)
    
    data = frappe.db.sql(f"""
        select
            mr.name as name,
            mr.status as mr_status,
            mr.transaction_date as transaction_date,
            mr_item.item_group as item_group,
            mr_item.item_code as item_code,
            mr_item.item_name as item_name,
            mr_item.description as item_description,
            mr_item.uom as uom,
            mr_item.qty as indent_qty,
            po.name as po_name,
            po.status as po_status,
            po.transaction_date as po_date,
            datediff(po.transaction_date, mr.transaction_date) as diff_indent_po_date,
            po_item.qty as po_qty,
            po_item.taxable_value as po_net_total,
            (po_item.taxable_value + po_item.igst_amount + po_item.cgst_amount + po_item.sgst_amount) as po_grand_total,
            (po_item.igst_amount + po_item.cgst_amount + po_item.sgst_amount) as tax_amount,
            (mr_item.qty - coalesce(po_item.qty, 0)) as balance_to_order,
            su.supplier_name as party_name,
            pr.transaction_date as advance_requested_date,
            pe.paid_amount as advance_approved,
            pe.posting_date as advance_paid_date,
            pe.total_allocated_amount as advance_paid,
            po.custom_delivery_days as po_delivery_days,
            po.status as delivery_status,
            po_item.received_qty as qty_received,
            (coalesce(po_item.qty, 0) - coalesce(po_item.received_qty, 0)) as qty_balance_to_received,
            purc.remarks as remarks,
            mr.status as indent_status,
            mr.custom_budget_code as budget_code,
            mr.custom_budget_amount as budget_amount,
            po.custom_site_indent_number as site_indent_no,
            (mr_item.qty - coalesce(po_item.qty, 0)) as balance_indent_qty,
            datediff(mr.modified, mr.creation) as diff_indent_creation_approval,
            datediff(po.transaction_date, mr.transaction_date) as diff_indent_po,
            (coalesce(po_item.qty, 0) - coalesce(po_item.received_qty, 0)) as variance,
            purc.custom_total_invoice_amount as purchase_invoice_value,
            (purc.grand_total - purc.custom_total_invoice_amount) as balance_purchase_invoice_value
        from
            `tabMaterial Request` mr
        left join
            `tabMaterial Request Item` mr_item on mr.name = mr_item.parent
        left outer join
            `tabPurchase Order Item` po_item on mr.name = po_item.material_request and mr_item.item_code = po_item.item_code
        left outer join
            `tabPurchase Order` po on po_item.parent = po.name
        left outer join
            `tabSupplier` su on po.supplier = su.name
        left outer join
            `tabPurchase Receipt Item` purc_item on po.name = purc_item.purchase_order
        left outer join
            `tabPurchase Receipt` purc on purc_item.parent = purc.name
        left outer join
            `tabPayment Request` pr on po.name = pr.reference_name
        left outer join
            `tabPayment Entry Reference` pe_re on po.name = pe_re.reference_name
        left outer join
            `tabPayment Entry` pe on pe_re.parent = pe.name
        where
            mr.docstatus = 1
            {condition}
        order by
            mr.transaction_date desc
    """, as_dict=1)
    
    # loop through the rows and get the first purchase receipt date and latest purchase receipt date where  purchase receipt item's field purchase order value is equal to the purchase order name 
    for row in data:
        first_receipt_date = frappe.db.sql(f"""
                                select
                                    min(purc.posting_date) as first_receipt_date,
                                    datediff(min(purc.posting_date), '{row.get('po_date')}') as calc_delivery_days
                                from
                                    `tabPurchase Receipt` purc
                                left join
                                    `tabPurchase Receipt Item` purc_item on purc.name = purc_item.parent
                                where
                                    purc_item.purchase_order = '{row.get('po_name')}'
                                """, as_dict=1)
        last_receipt_date = frappe.db.sql(f"""
                                select
                                    max(purc.posting_date) as last_receipt_date
                                from
                                    `tabPurchase Receipt` purc
                                left join
                                    `tabPurchase Receipt Item` purc_item on purc.name = purc_item.parent
                                where
                                    purc_item.purchase_order = '{row.get('po_name')}'
                                """, as_dict=1)
        
        # check if the po_status is closed or not if it is closed than set po_closed to True else False and do the same for indent_status
        if row.get('po_status') == 'Closed':
            row.update({"po_closed": "Yes"})
        else :
            row.update({"po_closed": "No"})
        
        if row.get('mr_status') == 'Closed':
            row.update({"indent_closed": "Yes"})
        else :
            row.update({"indent_closed": "No"})
        
        row.update({
            "first_delivery_date": first_receipt_date[0].get('first_receipt_date'),
            "last_delivery_date": last_receipt_date[0].get('last_receipt_date'),
            "calc_delivery_days": first_receipt_date[0].get('calc_delivery_days')
        })
    
    return data