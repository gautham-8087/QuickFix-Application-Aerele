# Copyright (c) 2026, Gautham  and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceInvoice(Document):
	def on_update(self):
		if self.payment_status == "Paid":
			if self.job_card:
				frappe.db.set_value(
					"Job Card", self.job_card, {"status": "Delivered", "payment_status": "Paid"}
				)


def has_permission(doc, user=None):
	import frappe

	user = user or frappe.session.user

	if "QF Manager" in frappe.get_roles(user):
		return True

	job_payment_status = frappe.db.get_value("Job Card", doc.job_card, "payment_status")

	if job_payment_status != "Paid":
		return False

	return True
