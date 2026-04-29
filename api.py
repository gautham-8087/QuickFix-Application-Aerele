import frappe
from frappe import _


def autoname(self):
	self.name = f"{self.part_code.upper()}"


def validate(self):
	if self.selling_price <= self.unit_cost:
		frappe.throw(_("Selling price must be greater than unit cost"))
