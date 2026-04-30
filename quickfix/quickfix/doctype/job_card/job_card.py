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

		for row in self.get("parts_used") or []:
			if (row.get("quantity") or 0) <= 0:
				frappe.throw(_("Quantity must be greater than 0 for {0}").format(row.get("part")))

			row.total_price = (row.get("quantity") or 0) * (row.get("unit_price") or 0)
			total += row.total_price

		self.parts_total = total
		self.final_amount = self.parts_total + (self.labour_charge or 0)

	def before_submit(self):
		if self.status != "Ready for Delivery":
			frappe.throw(_("Only Ready for Delivery jobs can be submitted"))


def permission_query_conditions(user):
	if "QF Technician" in frappe.get_roles(user):
		return f"""
			`tabJob Card`.assigned_technician IN (
				SELECT name FROM `tabTechnician`
				WHERE user = {frappe.db.escape(user)}
			)
		"""
