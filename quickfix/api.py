import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def customer_decision():
	job_card = frappe.form_dict.get("job_card")
	action = frappe.form_dict.get("action")

	if not job_card or not action:
		frappe.throw("Missing parameters")

	if not frappe.db.exists("Job Card", job_card):
		frappe.throw("Invalid Job Card")

	doc = frappe.get_doc("Job Card", job_card)

	# Prevent re-processing
	if doc.status in ["In Repair", "Cancelled"]:
		return {"status": "already_processed", "job_card": doc.name, "new_status": doc.status}

	if doc.status != "Awaiting Customer Approval":
		frappe.throw("This job is not awaiting customer approval")

	if action == "approve":
		doc.status = "In Repair"

	elif action == "reject":
		doc.status = "Cancelled"

	else:
		frappe.throw("Invalid action")

	doc.save(ignore_permissions=True)

	return {"status": "success", "job_card": doc.name, "new_status": doc.status}


@frappe.whitelist(allow_guest=True)
def get_job_details():
	job_card = frappe.form_dict.get("job_card")

	if not job_card:
		return None

	if not frappe.db.exists("Job Card", job_card):
		return None

	doc = frappe.get_doc("Job Card", job_card)

	return {
		"name": doc.name,
		"customer_name": doc.customer_name,
		"status": doc.status,
		"estimated_cost": doc.estimated_cost,
	}
