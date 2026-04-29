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

		total = 0

		for row in self.parts_used:
			if row.quantity <= 0:
				frappe.throw(f"Quantity must be greater than 0 for {row.part}")

			row.total_price = row.quantity * row.unit_price
			total += row.total_price

		self.parts_total = total

		# Optional but recommended
		self.final_amount = self.parts_total + (self.labour_charge or 0)

	def before_submit(self):
		if self.status != "Ready for Delivery":
			frappe.throw("Only Ready for Delivery jobs can be submitted")

	def on_submit(self):
		existing_invoice = frappe.db.exists("Service Invoice", {"job_card": self.name})

		if existing_invoice:
			return

		invoice = frappe.get_doc(
			{
				"doctype": "Service Invoice",
				"job_card": self.name,
				"labour_charge": self.labour_charge,
				"parts_total": self.parts_total,
				"total_amount": self.final_amount,
				"payment_status": "Unpaid",
			}
		)

		invoice.insert(ignore_permissions=True)
