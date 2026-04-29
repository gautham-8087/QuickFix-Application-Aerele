# Copyright (c) 2026, Gautham  and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		if not self.labour_charge:
			self.labour_charge = frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")

		if self.assigned_technician and self.status == "Draft":
			self.status = "Pending Diagnosis"

		if (
			self.diagnosis_notes
			and self.estimated_cost
			and self.diagnosis_date
			and self.status == "Pending Diagnosis"
		):
			self.status = "Awaiting Customer Approval"
