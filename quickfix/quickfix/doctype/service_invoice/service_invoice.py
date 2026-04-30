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
