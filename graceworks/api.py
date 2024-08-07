import frappe

@frappe.whitelist()
def get_order_qty(purchase_order_item):
    qty = frappe.db.get_value('Purchase Order Item', purchase_order_item, 'qty')
    return {'qty': qty}


import frappe

@frappe.whitelist()
def count_payment_requests(purchase_order):
    count = frappe.db.count('Payment Request', {
        'reference_name': purchase_order,
        'docstatus': ['!=', 2]
    })
    return {'count': count}


@frappe.whitelist()
def update_approved_advanced_requests(payment_request_name):
    try:
        payment_request = frappe.get_doc("Payment Request", payment_request_name)
        purchase_order = payment_request.reference_name

        approved_requests = frappe.get_all("Payment Request", 
            filters={
                "reference_doctype": "Purchase Order",
                "reference_name": purchase_order,
                "docstatus": 1  # Only approved payment requests
            },
            fields=["name", "grand_total","transaction_date"]
        )

        if not payment_request.meta.has_field("custom_approved_advanced_request"):
            frappe.throw("Child table 'custom_approved_advanced_request' not found in 'Payment Request' doctype.")

        payment_request.set("custom_approved_advanced_request", [])
        for req in approved_requests:
            payment_request.append("custom_approved_advanced_request", {
                "custom_payment_request": req.name,
                "custom_amount": req.grand_total,
                "custom_transaction_date": req.transaction_date
            })
        payment_request.save()
        return "Success"
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in update_approved_advanced_requests")
        frappe.throw(str(e))