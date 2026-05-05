import frappe


def after_install():
	# 1. Create Device Types (if not exists)
	for dt in ["Smartphone", "Laptop", "Tablet"]:
		if not frappe.db.exists("Device Type", dt):
			frappe.get_doc({"doctype": "Device Type", "device_type": dt}).insert(ignore_permissions=True)

	# 2. Create QuickFix Settings (Single)
	if not frappe.db.exists("QuickFix Settings", "QuickFix Settings"):
		frappe.get_doc(
			{
				"doctype": "QuickFix Settings",
				"shop_name": "QuickFix Service Centre",
				"manager_email": "admin@quickfix.com",
				"default_labour_charge": 500,
				"low_stock_alert_enabled": 1,
			}
		).insert(ignore_permissions=True)

	frappe.msgprint("QuickFix setup completed successfully")


def before_uninstall():
	submitted_jobs = frappe.db.exists("Job Card", {"docstatus": 1})

	if submitted_jobs:
		frappe.throw("Cannot uninstall: Submitted Job Cards exist")
