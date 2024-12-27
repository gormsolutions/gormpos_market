import frappe

@frappe.whitelist(allow_guest=True)
def print_invoice(invoice_id):
    # Fetch the Sales Invoice document
    res_doc = frappe.get_doc("Sales Invoice", invoice_id)
    
    # Fetch the full name of the logged-in user
    user_full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
    
    # Render the template with the additional user_full_name context
    context = {
        'doc': res_doc,
        'user_full_name': user_full_name
    }
    print_format = frappe.render_template("roots_app/templates/print_format/pos_invoice.html", context, is_path=True)
    
    return print_format
