import frappe


def get_shop_name():
	return frappe.get_single("QuickFix Settings").shop_name


def format_job_id(value):
	return f"JOB#{value}"
