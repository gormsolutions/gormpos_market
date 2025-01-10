import frappe

# @frappe.whitelist(allow_guest=True)
# def get_items(category=None, search_term=None):
#     try:
#         # Base query to fetch items
#         query = """
#             SELECT 
#                 i.item_code, 
#                 i.item_name, 
#                 i.image, 
#                 i.stock_uom, 
#                 i.item_group 
#             FROM `tabItem` i
#             LEFT JOIN `tabItem Barcode` ib ON i.item_code = ib.parent
#             LEFT JOIN `tabItem Group` ig ON i.item_group = ig.name
#             WHERE ig.parent_item_group = 'SuperMarkets'
#         """
#         conditions = []
#         values = {}

#         # Apply additional filters if category or search term is provided
#         if category:
#             conditions.append("i.item_group = %(category)s")
#             values["category"] = category

#         # Add search term filter for both item_name and barcode
#         if search_term:
#             conditions.append(""" 
#                 (i.item_name LIKE %(search_term)s OR ib.barcode LIKE %(search_term)s)
#             """)
#             values["search_term"] = f"%{search_term}%"

#         # Combine conditions with the base query
#         if conditions:
#             query += " AND " + " AND ".join(conditions)

#         # Execute the query
#         items = frappe.db.sql(query, values, as_dict=True)

#         # Format items with additional details
#         formatted_items = []
#         for item in items:
#             # Get the price from the Item Price doctype
#             price = frappe.db.get_value(
#                 "Item Price",
#                 {"item_code": item.item_code, "selling": 1},
#                 "price_list_rate"
#             ) or 0

#             # Fetch barcodes for the item
#             barcodes = frappe.get_all(
#                 "Item Barcode",
#                 fields=["barcode", "uom"],
#                 filters={"parent": item.item_code}
#             )
#             barcode = barcodes[0]["barcode"] if barcodes else ""
            
#             current_user = frappe.session.user
#             # Fetch User Permission records for 'Warehouse' allowed for the current user
#             warehouse_list = frappe.get_all(
#                 'User Permission',
#                     filters={
#                         'user': current_user,
#                         'allow': 'Warehouse'
#                 },
#                 fields=['for_value']
#             )
    
#             # Determine fallback warehouse
#             fallback_warehouse = warehouse_list[0]['for_value'] if warehouse_list else None


#             # Fetch the actual quantity from the Bin doctype
#             actual_qty = frappe.db.sql("""
#                 SELECT SUM(actual_qty) AS total_qty
#                 FROM `tabBin`
#                 WHERE item_code = %s
#             """, (item.item_code,), as_dict=True)[0].get("total_qty") or 0

#             formatted_items.append({
#                 "id": item.item_code,
#                 "name": item.item_name,
#                 "image": frappe.utils.get_url(item.image) if item.image else "",
#                 "uom": item.stock_uom,
#                 "price": price,
#                 "barcode": barcode,
#                 "item_group": item.item_group,
#                 "actual_qty": actual_qty,  # Include the actual quantity
#             })

#         # Fetch item groups for the dropdown that are under the 'SuperMarkets' parent
#         item_groups = frappe.get_all(
#             "Item Group",
#             fields=["name"],
#             filters={"parent_item_group": "SuperMarkets"}
#         )

#         return {
#             "items": formatted_items,
#             "fallback_warehouse": fallback_warehouse,
#             "item_groups": item_groups,
#         }

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Error Fetching Items")
#         return {"error": str(e)}

@frappe.whitelist(allow_guest=True)
def get_items(category=None, search_term=None):
    try:
        # Base query to fetch items
        query = """
            SELECT 
                i.item_code, 
                i.item_name, 
                i.image, 
                i.stock_uom, 
                i.item_group 
            FROM `tabItem` i
            LEFT JOIN `tabItem Barcode` ib ON i.item_code = ib.parent
            LEFT JOIN `tabItem Group` ig ON i.item_group = ig.name
            WHERE ig.parent_item_group = 'SuperMarkets'
        """
        conditions = []
        values = {}

        # Apply additional filters if category or search term is provided
        if category:
            conditions.append("i.item_group = %(category)s")
            values["category"] = category

        # Add search term filter for both item_name and barcode
        if search_term:
            conditions.append(""" 
                (i.item_name LIKE %(search_term)s OR ib.barcode LIKE %(search_term)s)
            """)
            values["search_term"] = f"%{search_term}%"

        # Combine conditions with the base query
        if conditions:
            query += " AND " + " AND ".join(conditions)

        # Execute the query
        items = frappe.db.sql(query, values, as_dict=True)
        current_user = frappe.session.user
        # Format items with additional details
        formatted_items = []
        for item in items:
            # Get the price from the Item Price doctype
            # Fetch User Permission records for 'Price List' allowed for the current user
            price_list = frappe.get_all(
                'User Permission',
                filters={
                'user': current_user,
                'allow': 'Price List',
                'is_default': 1
            },
            fields=['for_value']
            )

            permitted_price_list = price_list[0]['for_value'] if price_list else None

            price = frappe.db.get_value(
                "Item Price",
                {"item_code": item.item_code, "selling": 1, "price_list": permitted_price_list},
                "price_list_rate"
            ) or 0

            # Fetch barcodes for the item
            barcodes = frappe.get_all(
                "Item Barcode",
                fields=["barcode", "uom"],
                filters={"parent": item.item_code}
            )
            barcode = barcodes[0]["barcode"] if barcodes else ""
            
            
            # Fetch User Permission records for 'Warehouse' allowed for the current user
            warehouse_list = frappe.get_all(
                'User Permission',
                filters={
                'user': current_user,
                'allow': 'Warehouse'
            },
                fields=['for_value']
                )

            # Determine fallback warehouse
            fallback_warehouse = warehouse_list[0]['for_value'] if warehouse_list else None

            # Fetch the actual quantity from the Bin doctype for allowed warehouses
            actual_qty = frappe.db.sql("""
                SELECT SUM(actual_qty) AS total_qty
                FROM `tabBin`
                WHERE item_code = %s
                AND warehouse IN (%s)  -- Add filter for permitted warehouses
                """, (item.item_code, ','.join([str(warehouse['for_value']) for warehouse in warehouse_list])), as_dict=True)

            # Get the total quantity from the result or set it to 0 if none
            actual_qty = actual_qty[0].get("total_qty") if actual_qty else 0


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

        # Fetch item groups for the dropdown that are under the 'SuperMarkets' parent
        item_groups = frappe.get_all(
            "Item Group",
            fields=["name"],
            filters={"parent_item_group": "SuperMarkets"}
        )

        return {
            "items": formatted_items,
            "fallback_warehouse": fallback_warehouse,
            "item_groups": item_groups,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error Fetching Items")
        return {"error": str(e)}
