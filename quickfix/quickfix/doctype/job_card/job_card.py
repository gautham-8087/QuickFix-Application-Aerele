import frappe
from frappe import _
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		# Phone validation (safe)
		if not self.customer_phone or not (self.customer_phone.isdigit() and len(self.customer_phone) == 10):
			frappe.throw(_("Customer phone must be exactly 10 digits"))

		# Technician required
		if self.status in ["In Repair", "Ready for Delivery", "Delivered"]:
			if not self.assigned_technician:
				frappe.throw(_("Assigned Technician is required for this status"))

		# Estimated cost required
		if self.status == "In Repair" and not self.estimated_cost:
			frappe.throw(_("Estimated cost is required before starting repair"))

		# Compute parts
		total = 0
		for row in self.parts_used:
			if row.quantity <= 0:
				frappe.throw(_(f"Quantity must be > 0 for part {row.part}"))

			unit_price = row.unit_price or 0
			row.total_price = row.quantity * unit_price
			total += row.total_price

		self.parts_total = total

		# Labour charge fallback (safe)
		if self.labour_charge is None:
			self.labour_charge = frappe.db.get_value("QuickFix Settings", None, "default_labour_charge") or 0

		self.final_amount = self.parts_total + self.labour_charge

	def before_submit(self):
		if self.status != "Ready for Delivery":
			frappe.throw(_("Only Job Cards marked 'Ready for Delivery' can be submitted"))

		for row in self.parts_used:
			stock = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0

			if stock < row.quantity:
				frappe.throw(_(f"Not enough stock for part {row.part}. Available: {stock}"))

	def on_submit(self):
		# Deduct stock (system action)
		for row in self.parts_used:
			current_stock = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0

			frappe.db.set_value(
				"Spare Part",
				row.part,
				"stock_qty",
				current_stock - row.quantity,
				update_modified=False,
				ignore_permissions=True,
			)

		# Create invoice (avoid duplicates)
		existing_invoice = frappe.db.exists("Service Invoice", {"job_card": self.name})

		if not existing_invoice:
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

		# Realtime
		frappe.publish_realtime("job_ready", {"job_card": self.name}, user=self.owner)

		# Background email
		frappe.enqueue("quickfix.utils.send_job_ready_email", job_card=self.name, queue="short")

	def on_cancel(self):
		self.status = "Cancelled"

		for row in self.parts_used:
			current_stock = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0

			frappe.db.set_value(
				"Spare Part",
				row.part,
				"stock_qty",
				current_stock + row.quantity,
				update_modified=False,
				ignore_permissions=True,
			)

		invoice_name = frappe.db.get_value("Service Invoice", {"job_card": self.name})

		if invoice_name:
			invoice = frappe.get_doc("Service Invoice", invoice_name)
			if invoice.docstatus == 1:
				invoice.cancel()

	def on_trash(self):
		if self.status not in ["Draft", "Cancelled"]:
			frappe.throw(_("Only Draft or Cancelled Job Cards can be deleted"))


# -------------------------------
# Permission Query Conditions
# -------------------------------


def permission_query_conditions(user):
	if "QF Technician" in frappe.get_roles():
		return f"""
            `tabJob Card`.assigned_technician IN (
                SELECT name FROM `tabTechnician`
                WHERE user = {frappe.db.escape(user)}
            )
        """
	return ""
