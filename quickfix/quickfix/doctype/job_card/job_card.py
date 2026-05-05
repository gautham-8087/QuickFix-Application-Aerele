import frappe
from frappe import _
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		if not self.customer_phone or not (self.customer_phone.isdigit() and len(self.customer_phone) == 10):
			frappe.throw(_("Customer phone must be exactly 10 digits"))

		if self.status in ["In Repair", "Ready for Delivery", "Delivered"]:
			if not self.assigned_technician:
				frappe.throw(_("Assigned Technician is required for this status"))

		if self.status == "In Repair" and not self.estimated_cost:
			frappe.throw(_("Estimated cost is required before starting repair"))

		total = 0
		for row in self.parts_used or []:
			if row.quantity <= 0:
				frappe.throw(_("Quantity must be > 0 for part {0}").format(row.part))

			unit_price = row.unit_price or 0
			row.total_price = row.quantity * unit_price
			total += row.total_price

		self.parts_total = total

		if self.labour_charge is None:
			self.labour_charge = frappe.db.get_single_value("QuickFix Settings", "default_labour_charge") or 0

		self.final_amount = self.parts_total + self.labour_charge

		print("Controller validate")

	def before_submit(self):
		if self.status != "Ready for Delivery":
			frappe.throw(_("Only Job Cards marked 'Ready for Delivery' can be submitted"))

		for row in self.parts_used or []:
			stock = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0

			if stock < row.quantity:
				frappe.throw(_("Not enough stock for part {0}. Available: {1}").format(row.part, stock))

	def on_cancel(self):
		self.db_set("status", "Cancelled")

		for row in self.parts_used or []:
			current_stock = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0

			frappe.db.set_value(
				"Spare Part",
				row.part,
				"stock_qty",
				current_stock + row.quantity,
				update_modified=False,
				ignore_permissions=True,
			)


def permission_query_conditions(user):
	if "QF Technician" in frappe.get_roles():
		return f"""
            `tabJob Card`.assigned_technician IN (
                SELECT name FROM `tabTechnician`
                WHERE user = {frappe.db.escape(user)}
            )
        """
	return ""
