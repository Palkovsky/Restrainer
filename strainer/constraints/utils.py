import re
import numbers

email_reg = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_email(string):
	try:
		return re.match(email_reg, string) != None
	except:
		return False

def data_to_string_type(data):
	if isinstance(data, str):
		return "string"
	elif isinstance(data, bool):
		return "boolean"
	elif isinstance(data, numbers.Number):
		return "numeric"
	elif isinstance(data, list):
		return "list"
	elif isinstance(data, dict):
		return "dictionary"
	elif isinstance(data, None):
		return "null"
	return None