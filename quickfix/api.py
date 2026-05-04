import frappe
from frappe import _


@frappe.whitelist()
def customer_decision():
	job_card = frappe.form_dict.get("job_card")
	action = frappe.form_dict.get("action")

	if not job_card or not action:
		frappe.throw(_("Missing parameters"))

	if not frappe.db.exists("Job Card", job_card):
		frappe.throw(_("Invalid Job Card"))

	doc = frappe.get_doc("Job Card", job_card)

	if doc.status in ["In Repair", "Cancelled"]:
		return {"status": "already_processed", "job_card": doc.name, "new_status": doc.status}

	if doc.status != "Awaiting Customer Approval":
		frappe.throw(_("This job is not awaiting customer approval"))

	if action == "approve":
		doc.status = "In Repair"

	elif action == "reject":
		doc.status = "Cancelled"

	else:
		frappe.throw(_("Invalid action"))

	doc.save()

	return {"status": "success", "job_card": doc.name, "new_status": doc.status}


@frappe.whitelist()
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


@frappe.whitelist()
def share_job_card(job_card_name: str, user_email: str) -> str:
	frappe.share.add(doctype="Job Card", name=job_card_name, user=user_email, read=1, write=0, share=0)
	return "Shared successfully"


@frappe.whitelist()
def Manager_only_action():
	frappe.only_for("QF Manager")
	return "You are allowed"


@frappe.whitelist()
def get_job_cards_unsafe():
	return frappe.get_all("Job Card", fields="*")


@frappe.whitelist()
def get_job_cards_safe():
	import frappe

	user = frappe.session.user
	is_manager = "QF Manager" in frappe.get_roles(user)

	fields = ["name", "customer_name", "status", "assigned_technician", "final_amount"]

	if is_manager:
		fields += ["customer_phone", "customer_email"]

	return frappe.get_list("Job Card", fields=fields)


@frappe.whitelist()
def rename_technician(old_name: str, new_name: str) -> None:
	frappe.rename_doc("Technician", old_name, new_name, merge=False)


# When combining the two documents into one, so merge = true would be dangerous. The reason is data loss due to merging.
