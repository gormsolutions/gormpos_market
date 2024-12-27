import frappe

@frappe.whitelist(allow_guest=True)
def get_items(category=None, search_term=None):
    try:
        # Base query
        query = """
            SELECT 
                i.item_code, 
                i.item_name, 
                i.image, 
                i.stock_uom, 
                i.item_group 
            FROM `tabItem` i
            LEFT JOIN `tabItem Barcode` ib ON i.item_code = ib.parent
            WHERE 1=1
        """
        conditions = []
        values = {}

        # Add category filter
        if category:
            conditions.append("i.item_group = %(category)s")
            values["category"] = category

        # Add search term filter for both item_name and barcode
        if search_term:
            conditions.append("""
                (i.item_name LIKE %(search_term)s OR ib.barcode LIKE %(search_term)s)
            """)
            values["search_term"] = f"%{search_term}%"

        # Combine conditions
        if conditions:
            query += " AND " + " AND ".join(conditions)

        # Execute query
        items = frappe.db.sql(query, values, as_dict=True)

        # Format items with additional details
        formatted_items = []
        for item in items:
            # Get the price from the Item Price doctype
            price = frappe.db.get_value(
                "Item Price",
                {"item_code": item.item_code, "selling": 1},
                "price_list_rate"
            ) or 0

            # Fetch barcodes for the item
            barcodes = frappe.get_all(
                "Item Barcode",
                fields=["barcode", "uom"],
                filters={"parent": item.item_code}
            )
            barcode = barcodes[0]["barcode"] if barcodes else ""

            # Fetch the actual quantity from the Bin doctype
            actual_qty = frappe.db.sql("""
                SELECT SUM(actual_qty) AS total_qty
                FROM `tabBin`
                WHERE item_code = %s
            """, (item.item_code,), as_dict=True)[0].get("total_qty") or 0

            formatted_items.append({
                "id": item.item_code,
                "name": item.item_name,
                "image": frappe.utils.get_url(item.image) if item.image else "",
                "uom": item.stock_uom,
                "price": price,
                "barcode": barcode,
                "item_group": item.item_group,
                "actual_qty": actual_qty,  # Include the actual quantity
            })

        # Fetch all item groups for the dropdown
        item_groups = frappe.get_all("Item Group", fields=["name"])

        return {
            "items": formatted_items,
            "item_groups": item_groups,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error Fetching Items")
        return {"error": str(e)}
