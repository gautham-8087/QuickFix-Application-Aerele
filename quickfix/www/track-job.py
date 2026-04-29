import frappe


def get_context(context):
	context.job = None

	job_card = frappe.form_dict.get("job_card")

	if job_card:
		doc = frappe.get_doc("Job Card", job_card)

		context.job = {
			"name": doc.name,
			"status": doc.status,
			"customer_name": doc.customer_name,
			"estimated_cost": doc.estimated_cost,
		}

	return context
