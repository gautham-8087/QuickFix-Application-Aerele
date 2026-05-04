import unittest

import frappe


class TestJobCardOverride(unittest.TestCase):
	def test_validate_calls_super(self):
		jc = frappe.get_doc(
			{
				"doctype": "Job Card",
				"customer_name": "Test",
				"customer_phone": "1234567890",
				"device_type": "Phone",
				"problem_description": "Test issue",
			}
		)

		jc.insert()

		# This depends on base logic running
		self.assertIsNotNone(jc.final_amount)
