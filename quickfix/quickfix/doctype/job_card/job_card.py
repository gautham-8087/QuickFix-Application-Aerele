import frappe
from frappe import _
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

		for row in self.parts_used or []:
			if row.quantity <= 0:
				frappe.throw(_("Quantity must be greater than 0 for {0}").format(row.part))

			row.total_price = (row.quantity or 0) * (row.unit_price or 0)
			total += row.total_price

		self.parts_total = total
		self.final_amount = self.parts_total + (self.labour_charge or 0)

	def before_submit(self):
		if self.status != "Ready for Delivery":
			frappe.throw(_("Only Ready for Delivery jobs can be submitted"))
