import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class SparePart(Document):
	def autoname(self):
		if not self.part_code:
			frappe.throw(_("Part Code is required"))

		# Ensure uppercase
		self.part_code = self.part_code.upper()

		# Incorporate part_code into the name, e.g. PART-2024-0001-ENGINEOIL
		self.name = make_autoname("PART-.YYYY.-.####.-" + self.part_code)

	def on_update(self):
		threshold = frappe.db.get_single_value("Quick Settings", None, "low_stock_threshold")

		if threshold and self.stock_qty <= threshold:
			frappe.msgprint(
				f"Warning: {self.part_name} is at or below the low stock threshold ({threshold}).", alert=True
			)
