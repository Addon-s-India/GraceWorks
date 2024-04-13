frappe.ui.form.on("Purchase Order", {
    before_submit: function (frm) {
        if (!check_if_image_empty(frm)) {
            frappe.validated = false;
        }
    },
    onload: function (frm) {
        mandatory_fields(frm);
    },
    refresh: function (frm) {
        mandatory_fields(frm);
    },
});

function mandatory_fields(frm) {
    // check if frm.doc.name exist in database or not and if doc is saved and exist  then make the fields mandatory
    if (!frm.doc.__islocal) {
        console.log("in mandatory fields");
        // frm.fields_dict.items.grid.toggle_reqd("image", true);
        // frm.fields_dict.items.grid.toggle_reqd("custom_image_1", true);
        // frm.fields_dict.items.grid.toggle_reqd("custom_image_2", true);
        frm.toggle_reqd("custom_attach_file", true);
    }
}

function check_if_image_empty(frm) {
    // let items = frm.doc.items;
    // let flag = 0;
    // for (let i = 0; i < items.length; i++) {
    //     if (
    //         !items[i].image ||
    //         !items[i].custom_image_1 ||
    //         !items[i].custom_image_2
    //     ) {
    //         flag = 1;
    //         break;
    //     }
    // }
    // if (flag == 1) {
    //     // frappe.msgprint("Please fill all the images in the items table");
    //     frappe.throw("Please fill all the images in the items table");
    //     return false;
    // } else {
    //     return true;
    // }
    if (!frm.doc.custom_attach_file) {
        frappe.throw("Please attach the file");
        return false;
    } else {
        return true;
    }
}
