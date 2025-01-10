import frappe
@frappe.whitelist()
def create_invoice(paid_amount, items,custom_cash_given, customer_name=None,user=None, is_pos=None, update_stock=None):
    import json

    # Parse items if necessary
    if isinstance(items, str):
        items = json.loads(items)

    # Get the current user
    current_user = frappe.session.user

    # Fetch User Permission records for 'Warehouse' allowed for the current user
    fallback_warehouse = frappe.get_all(
        'User Permission',
        filters={
            'user': current_user,
            'allow': 'Warehouse'
        },
        fields=['for_value']
    )

    # Determine the fallback warehouse value
    fallback_warehouse = fallback_warehouse[0]['for_value'] if fallback_warehouse else None

    if not fallback_warehouse:
        # Set a default warehouse if no user permissions are found
        fallback_warehouse = frappe.db.get_single_value('Stock Settings', 'default_warehouse')
        if not fallback_warehouse:
            return {"error": "No warehouse assigned to user and no default warehouse found in Stock Settings."}

    pos_profile = None
    pos_warehouse = None

    # If user is provided and is_pos is enabled, fetch POS profile
    if user and is_pos:
        pos_profile = frappe.db.get_value("POS Profile User", {"default": 1, "user": user}, "parent")
        pos_warehouse = frappe.db.get_value("POS Profile", pos_profile, "warehouse")

    # Set warehouse and enable update_stock if is_pos or update_stock is enabled
    if is_pos or update_stock:
        for item in items:
            # Use POS warehouse if available, else fallback to user-defined or default warehouse
            item['warehouse'] = pos_warehouse or fallback_warehouse
        update_stock = 1  # Explicitly enable update_stock

    try:
        # Construct the Sales Invoice document
        invoice_doc_data = {
            "doctype": "Sales Invoice",
            "customer": "Cash Customer",
            "custom_cash_given":custom_cash_given,
            # "from_mobile_app": "Mobile App Cash Customer",
            "update_stock": update_stock,  # Ensure update_stock is enabled
            "is_pos": is_pos,  # Use the value passed by the user
            "is_paid": 1,  # Include is_paid with a default value of 1
            "items": items,
            "payment_terms_template": frappe.db.get_value("Customer", customer_name, "payment_terms") or None
        }

        # Include POS profile only if is_pos is enabled
        if is_pos:
            invoice_doc_data["pos_profile"] = pos_profile

            # Add payment details for POS invoices
            invoice_doc_data["payments"] = [{
                "mode_of_payment": "Cash",
                "amount": paid_amount
            }]

        invoice_doc = frappe.get_doc(invoice_doc_data)

        # Save and submit the document
        res_doc = invoice_doc.insert()
        res_doc.submit()
        return res_doc

    except Exception as e:
        return {"error": str(e)}
