import re

email_reg = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_email(string):
	try:
		return re.match(email_reg, string) != None
	except:
		return False