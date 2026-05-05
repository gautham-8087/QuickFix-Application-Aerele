import frappe


def log_change(doc, method):
	if doc.doctype == "Audit Log":
		return

	frappe.get_doc(
		{
			"doctype": "Audit Log",
			"doctype_name": doc.doctype,
			"document_name": doc.name,
			"action": method,
			"user": frappe.session.user,
			"timestamp": frappe.utils.now(),
		}
	).insert(ignore_permissions=True)


def log_login(login_manager):
	frappe.get_doc(
		{
			"doctype": "Audit Log",
			"doctype_name": "Session",
			"document_name": frappe.session.user,
			"action": "login",
			"user": frappe.session.user,
			"timestamp": frappe.utils.now(),
		}
	).insert(ignore_permissions=True)


def log_logout(login_manager):
	frappe.get_doc(
		{
			"doctype": "Audit Log",
			"doctype_name": "Session",
			"document_name": frappe.session.user,
			"action": "logout",
			"user": frappe.session.user,
			"timestamp": frappe.utils.now(),
		}
	).insert(ignore_permissions=True)
