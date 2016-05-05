import re, numbers, socket


email_reg = re.compile(r"[^@]+@[^@]+\.[^@]+")
mac_reg = re.compile(r"[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$")

def is_email(string):
	try:
		return re.match(email_reg, string) != None
	except:
		return False

def is_ip(string):
	try:
		print(string)
		socket.inet_aton(string)
		return True
	except socket.error:
		return False

def is_mac(string):
	if re.match(mac_reg, string.lower()):
		return True
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