import frappe

@frappe.whitelist()
def get_order_qty(purchase_order_item):
    qty = frappe.db.get_value('Purchase Order Item', purchase_order_item, 'qty')
    return {'qty': qty}