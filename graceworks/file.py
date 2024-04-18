import frappe

def on_delete(doc, method):
    # delete the attachment from the file manager
    # if the attached_to_doctype is Purchase Order and the attached_to_name doc is submmited then dont allow to delete the document and throw error
    if doc.attached_to_doctype == "Purchase Order":
        po = frappe.get_doc("Purchase Order", doc.attached_to_name)
        if po.docstatus == 1:
            frappe.throw("Cannot delete the attachment as the Purchase Order is submitted")
    