import frappe
from frappe import _


def autoname(self):
	self.name = f"{self.part_code.upper()}"


def validate(self):
	if self.selling_price <= self.unit_cost:
		frappe.throw(_("Selling price must be greater than unit cost"))


@frappe.whitelist(allow_guest=True)
def customer_decision():
	# Get inputs safely
	job_card = frappe.form_dict.get("job_card")
	action = frappe.form_dict.get("action")

	# Basic validation
	if not job_card or not action:
		frappe.throw("Missing parameters")

	if not frappe.db.exists("Job Card", job_card):
		frappe.throw("Invalid Job Card")

	# Fetch document
	doc = frappe.get_doc("Job Card", job_card)

	# Ensure correct stage
	if doc.status != "Awaiting Customer Approval":
		frappe.throw("This job is not awaiting customer approval")

	# Apply decision
	if action == "approve":
		doc.status = "In Repair"

	elif action == "reject":
		doc.status = "Cancelled"

	else:
		frappe.throw("Invalid action")

	# Save with system override
	doc.save(ignore_permissions=True)

	return {"status": "success", "job_card": doc.name, "new_status": doc.status}
