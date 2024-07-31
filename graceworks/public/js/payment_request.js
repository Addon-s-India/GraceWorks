frappe.ui.form.on("Payment Request", {
    onload: function (frm) {
        frm.toggle_reqd("transaction_date", true);
        console.log("onload");
        if (
            frm.doc.reference_doctype == "Purchase Order" &&
            frm.doc.docstatus == 0
        ) {
            read_only(frm);
            update_amount_po(frm);
            fetch_po_date(frm);
        }
    },
    refresh: function (frm) {
        frm.toggle_reqd("transaction_date", true);
        console.log("refresh");
        if (
            frm.doc.reference_doctype == "Purchase Order" &&
            frm.doc.docstatus == 0
        ) {
            read_only(frm);
            update_amount_po(frm);
            fetch_po_date(frm);
        }
    },
    reference_name: function (frm) {
        fetch_po_date(frm);
        fetch_project(frm);
    },
    custom_type_of_amount: function (frm) {
        update_amount_po(frm);
    },
    custom_add_amount_based_on: function (frm) {
        if (frm.doc.custom_add_amount_based_on == "Percent") {
            // clear custom_lumpsum_amount field
            frm.set_value("custom_lumpsum_amount", 0);
            frm.set_value("grand_total", 0);
        } else {
            // clear custom_percent_amount field
            frm.set_value("custom_percent_value", 0);
            frm.set_value("grand_total", 0);
        }
    },
    custom_percent_value: function (frm) {
        if (frm.doc.custom_percent > 100) {
            frappe.msgprint("Percent should not be greater than 100");
            frm.set_value("custom_percent_value", 0);
        } else {
            // calculate the amount based on the custom_amount_from_po field
            const amount = frm.doc.custom_type_of_amount == "Including Tax"
                ? frm.doc.custom_amount_from_po
                : frm.doc.custom_amount_from_po_excluding_tax;
            const percent = frm.doc.custom_percent_value;
            console.log("amount :: ", amount);
            console.log("percent :: ", percent);
            const total = (amount * percent) / 100;
            console.log("total :: ", total);
            if (total > amount) {
                frappe.throw(
                    "Total amount should not be greater than pending amount"
                );
                frm.set_value("custom_percent_value", 0);
                frm.set_value("grand_total", 0);
            } else {
                frm.set_value("grand_total", total);
            }
        }
    },
    custom_lumpsum_amount: function (frm) {
        // calculate the amount based on the custom_amount_from_po field
        const amount = frm.doc.custom_type_of_amount == "Including Tax"
            ? frm.doc.custom_amount_from_po
            : frm.doc.custom_amount_from_po_excluding_tax;
        if (frm.doc.custom_lumpsum_amount > amount) {
            frappe.throw(
                "Lumpsum amount should not be greater than pending amount"
            );
            frm.set_value("custom_lumpsum_amount", 0);
            frm.set_value("grand_total", 0);
        } else {
            frm.set_value("grand_total", frm.doc.custom_lumpsum_amount);
        }
    },
    validate: function (frm) {
        if (!check_payment_request_pending_for_the_po(frm)) {
            frappe.validated = false; // This line ensures form doesn't submit
        }
        check_grand_total(frm);
    },
});

function read_only(frm) {
    // make amount field read only
    if (frm.doc.reference_doctype == "Purchase Order") {
        // frm.toggle_enable("amount", false);
        frm.set_df_property("grand_total", "read_only", 1);
        if (
            (!frm.doc.custom_percent_value &&
                frm.doc.custom_add_amount_based_on == "Percent") ||
            (!frm.doc.custom_lumpsum_amount &&
                frm.doc.custom_add_amount_based_on == "Lumpsum Amount")
        ) {
            frm.set_value("grand_total", 0);
        }
    }
}

async function update_amount_po(frm) {
    try {
        let totalFromPO = 0;
        let amountFromPOExcludingTax = 0;
        let amountFromPOIncludingTax = 0;

        const grandTotalRes = await frappe.db.get_value(
            frm.doc.reference_doctype,
            frm.doc.reference_name,
            "grand_total"
        );
        amountFromPOIncludingTax = grandTotalRes.message.grand_total;
        frm.set_value("custom_amount_from_po", amountFromPOIncludingTax);

        const totalRes = await frappe.db.get_value(
            frm.doc.reference_doctype,
            frm.doc.reference_name,
            "total"
        );
        amountFromPOExcludingTax = totalRes.message.total;
        frm.set_value(
            "custom_amount_from_po_excluding_tax",
            amountFromPOExcludingTax
        );

        // Check the type of amount and fetch the corresponding total
        if (frm.doc.custom_type_of_amount == "Including Tax") {
            totalFromPO = amountFromPOIncludingTax;
        } else if (frm.doc.custom_type_of_amount == "Excluding Tax") {
            totalFromPO = amountFromPOExcludingTax;
        }

        // Fetch the grand totals from all submitted Payment Requests related to the PO
        const paymentRequests = await frappe.db.get_list("Payment Request", {
            filters: {
                reference_doctype: frm.doc.reference_doctype,
                reference_name: frm.doc.reference_name,
                docstatus: 1, // Only consider submitted payment requests
            },
            fields: ["grand_total"],
        });

        // Calculate the sum of all fetched payment requests' grand totals
        const totalPaid = paymentRequests.reduce(
            (sum, pr) => sum + (pr.grand_total || 0),
            0
        );
        frm.set_value("custom_request_amount_approved", totalPaid);
        // Subtract the total paid from the total fetched from the PO
        const remainingAmount = totalFromPO - totalPaid;

        // Set the computed value to the custom field on the form
        frm.set_value("custom_amount_pending", remainingAmount);
    } catch (error) {
        console.error("Error in updating amount from PO:", error);
        frappe.msgprint(
            "There was an error updating the payment amounts. Please check the console for more details."
        );
    }
}

async function check_payment_request_pending_for_the_po(frm) {
    if (!frm.doc.__islocal && frm.doc.name) {
        // Check only if the document has been saved at least once (not new)
        try {
            const res = await frappe.db.get_list("Payment Request", {
                filters: {
                    reference_doctype: frm.doc.reference_doctype,
                    reference_name: frm.doc.reference_name,
                    docstatus: 0, // Only fetch entries that are not submitted
                    name: ["!=", frm.doc.name], // Exclude current document if it's already saved
                },
                fields: ["name"], // Only fetch the 'name' field
            });

            // Check if there are any pending payment requests other than the current one
            if (res.length) {
                let message =
                    "<b>Following Payment Request are pending for this Purchase Order:</b>";
                res.forEach((pr) => {
                    message += `<br> <b>${pr.name}</b>`;
                });
                frappe.msgprint(message);
                // prevent form submission by throwing an error
                throw new frappe.ValidationError();
            }
        } catch (error) {
            console.error("Error checking pending payment requests", error);
            throw error; // Rethrow to ensure form doesn't submit
        }
    }
}

function check_grand_total(frm) {
    if (frm.doc.grand_total <= 0) {
        frappe.msgprint("Grand Total should be greater than 0");
        frappe.validated = false;
    }
}

function fetch_po_date(frm) {
    console.log("fetch_po_date");
    if (
        frm.doc.reference_doctype === "Purchase Order" &&
        frm.doc.reference_name &&
        frm.doc.docstatus !== 1
    ) {
        console.log("fetch_po_date condition true");
        // fetch the date from the purchase order using the reference name
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Purchase Order",
                name: frm.doc.reference_name,
            },
            callback: function (r) {
                if (r.message) {
                    frm.set_value("custom_po_date", r.message.transaction_date);
                    const project_value = r.message.items[0].project;
                    frm.set_value("project", project_value);
                }
            },
        });
    }
}
