frappe.ui.form.on("Purchase Order", {
    before_submit: function (frm) {
        if (!check_if_image_empty(frm)) {
            frappe.validated = false;
        }
    },
    onload: function (frm) {
        mandatory_fields(frm);
        toggle_required(frm);
    },
    refresh: function (frm) {
        toggle_required(frm);
        mandatory_fields(frm);
        fetch_material_item_qty(frm);
    },
    // items_on_form_rendered: function (frm) {
    //     console.log("items_on_form_rendered");
    //     fetch_material_item_qty(frm);
    // },
    // before_save: function (frm) {
    //     console.log("before_save");
    //     fetch_material_item_qty(frm);
    // },
});

function mandatory_fields(frm) {
    // check if frm.doc.name exist in database or not and if doc is saved and exist  then make the fields mandatory
    if (!frm.doc.__islocal) {
        frm.toggle_reqd("custom_attach_file", true);
    }
}

function check_if_image_empty(frm) {
    if (!frm.doc.custom_attach_file) {
        frappe.throw("Please attach the file");
        return false;
    } else {
        return true;
    }
}

function fetch_material_item_qty(frm) {
    // loop through al items and get the item qty from the material request
    if (frm.doc.docstatus !== 1) {
        console.log("fetch_material_item_qty");
        let items = frm.doc.items;
        for (let i = 0; i < items.length; i++) {
            if (!items[i].material_request) {
                continue;
            }
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Material Request",
                    filters: {
                        name: items[i].material_request,
                    },
                },
                callback: function (data) {
                    console.log(
                        "Response of material request item :: ",
                        data.message
                    );
                    let item_qty = data.message.items.find(
                        (item) => item.item_code === items[i].item_code
                    );
                    console.log("item_qty :: ", item_qty);
                    frappe.model.set_value(
                        items[i].doctype,
                        items[i].name,
                        "custom_material_request_item_qty",
                        item_qty.qty
                    );
                },
            });
        }
    }
}

function toggle_required(frm) {
    // frm.toggle_reqd("project", true);
    frm.toggle_reqd("set_warehouse", true);
    frm.toggle_reqd("schedule_date", true);
    frm.toggle_reqd("custom_reference_no", true);
    frm.toggle_reqd("custom_reference_date", true);
    frm.toggle_reqd("custom_contact_person_at_site", true);

    // make the rate field in item table mandatory
    frm.fields_dict.items.grid.toggle_reqd("rate", true);
    frm.fields_dict.items.grid.toggle_reqd("project", true);
}
