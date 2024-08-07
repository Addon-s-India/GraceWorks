frappe.ui.form.on('Payment Request', {
    before_save: function(frm) {
        if (frm.doc.reference_name) {
            frappe.call({
                method: 'graceworks.api.count_payment_requests',
                args: {
                    purchase_order: frm.doc.reference_name
                },
                callback: function(r) {
                    if (r.message) {
                        let count = r.message.count + 1; // increment count for the new request
                        frm.set_value('custom_payment_request_number', count);
                        frappe.msgprint({
                            title: __('Payment Request Count'),
                            indicator: 'blue',
                            message: __('This is the {0} payment request for this Purchase Order.', [count])
                        });
                    }
                }
            });
        }
    }
});
