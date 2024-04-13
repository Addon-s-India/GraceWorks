import frappe

def po_before_submit(doc, method):
    # check if the custom_attach_file field is set or not if not then throw error and stop submission
    if not doc.custom_attach_file:
        frappe.throw("Please attach the file before submission")
        
    # if there is no attachment on image, custom_image_1 and custom_image_2 in items table then throw error and stop submission
    # for item in doc.items:
    #     if or item.image or not item.custom_image_1 or not item.custom_image_2:
    #         frappe.throw("Please attach the image before submission")