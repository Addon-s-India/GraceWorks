import frappe
from frappe.utils import logger
from erpnext.controllers.queries import get_match_cond

logger.set_log_level('DEBUG')
logger = frappe.logger("graceworks", allow_site=True, file_count=10)

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def custom_item_query(doctype, txt, searchfield, start, page_len, filters):
    from_warehouse = filters.get('from_warehouse')
    logger.info(f"from_warehouse: {from_warehouse}")

    return frappe.db.sql("""
        SELECT tabItem.name, tabItem.item_name, tabBin.actual_qty
        FROM `tabItem`
        JOIN `tabBin` ON tabItem.name = tabBin.item_code
        WHERE tabBin.warehouse = %(warehouse)s
            AND tabBin.actual_qty > 0
            AND (tabItem.name LIKE %(txt)s OR tabItem.item_name LIKE %(txt)s)
        ORDER BY
            IF(LOCATE(%(_txt)s, tabItem.name), LOCATE(%(_txt)s, tabItem.name), 99999),
            IF(LOCATE(%(_txt)s, tabItem.item_name), LOCATE(%(_txt)s, tabItem.item_name), 99999),
            tabItem.name, tabItem.item_name
        LIMIT %(start)s, %(page_len)s
    """, {
        'warehouse': from_warehouse,
        'txt': "%{}%".format(txt),
        '_txt': txt.replace("%", ""),
        'start': start,
        'page_len': page_len
    })


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def custom_stock_entry_type_query(doctype, txt, searchfield, start, page_len, filters):
    # give only "Material Issue" in the query result
    return frappe.db.sql("""
        SELECT name
        FROM `tabStock Entry Type`
        WHERE name = 'Material Issue' OR name = 'Material Transfer'
            AND (name LIKE %(txt)s OR {key} LIKE %(txt)s)
            {mcond}
        ORDER BY
            IF(LOCATE(%(_txt)s, name), LOCATE(%(_txt)s, name), 99999),
            name
        LIMIT %(start)s, %(page_len)s
    """.format(**{
        'key': searchfield,
        'mcond': get_match_cond(doctype)
    }), {
        'txt': "%{}%".format(txt),
        '_txt': txt.replace("%", ""),
        'start': start,
        'page_len': page_len
    })