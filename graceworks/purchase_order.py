import frappe

def po_before_submit(doc, method):
    # check if the custom_attach_file field is set or not if not then throw error and stop submission
    if not doc.custom_attach_file:
        frappe.throw("Please attach the file before submission")