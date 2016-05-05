import numbers, re
from abc import ABCMeta, abstractmethod, abstractproperty
from restrainer.constraints.utils import is_email, data_to_string_type, is_ip, is_mac
from restrainer.constraints.exceptions import *

class Constraint(metaclass=ABCMeta):

	def __init__(self):
		pass


	'''
		property identifying constraint in scheme definition
		Ex.

		"name" : {
			"type" : "string" - 'type' is name here
		}
	'''
	@property
	def name(self):
		pass

	'''
		For most cases this should stay False. It may True when it don't matter if user data is null.
		Ex. required constraint should allow this
	'''
	@property
	def accept_null(self):
	    return False

	'''
		This method decides if validation is successful or not.

		value - passed field value
		constraint_value - value of key in scheme(key is name property)

		It shall return True or False depending on validation status.
		Although returning dictionary will result in False, because dictionary key, value pairs
		will be shown as additional info in error message.
	'''
	@abstractmethod
	def validate(self, value, constraint_value, field_name, doc):
		pass

class TypeConstraint(Constraint):

	def __init__(self):
		super(TypeConstraint, self).__init__()
		self._types = {
			"integer" : int,
			"float" : float,
			"string" : str,
			"boolean" : bool,
			"list" : list,
			"object" : dict,
			"numeric" : numbers.Number
		}
	

	def register_type(self, name, cls):
		for key, type in self._types.items():
			if name in self._types:
				raise ConstrainException("Name '" + key + "' already registered.")
		self._types[name] = cls

	def name(self):
		return "type"

	def validate(self, value, constraint_value, field_name, doc):
		for key, type in self._types.items():
			if constraint_value == key and not isinstance(value, type):
				return {"type" : key}
		return True

class ListTypeConstraint(TypeConstraint):

	def __init__(self):
		super(ListTypeConstraint, self).__init__()

	def name(self):
		return "list_type"

	def validate(self, value, constraint_value, field_name, doc):
		try:
			for item in value:
				for key, type in self._types.items():
					if constraint_value == key and not isinstance(item, type):
						return {"list_type" : constraint_value}
			return True
		except:
			return {"list_type" : constraint_value}

class ExsitanceConstraint(Constraint):

	def __init__(self):
		super(Constraint, self).__init__()

	def name(self):
		return "required"

	def accept_null(self):
	    return True

	def validate(self, value, constraint_value, field_name, doc):
		if constraint_value == True:
			return value != None
		return True


class ValueConstraint(Constraint):

	def __init__(self):
		super(ValueConstraint, self).__init__()
	
	def name(self):
		return "value"

	def validate(self, value, constraint_value, field_name, doc):
		if not value in constraint_value:
			return {"allowed" : constraint_value}
		return True
		
class MinConstraint(Constraint):

	def __init__(self):
		super(MinConstraint, self).__init__()

	def name(self):
		return "min"

	def validate(self, value, constraint_value, field_name, doc):
		min = constraint_value
		if isinstance(value, numbers.Number):
			if value < min:
				return {"min" : min}
		elif isinstance(value, str) or isinstance(value, list) or isinstance(value, dict):
			if len(value) < min:
				return {"min" : min}
		return True	

class MaxConstraint(Constraint):

	def __init__(self):
		super(MaxConstraint, self).__init__()

	def name(self):
		return "max"

	def validate(self, value, constraint_value, field_name, doc):
		max = constraint_value
		if isinstance(value, numbers.Number):
			if value > max:
				return {"max" : max}
		elif isinstance(value, str) or isinstance(value, list) or isinstance(value, dict):
			if len(value) > max:
				return {"max" : max}
		return True	

class BetweenConstraint(Constraint):

	def __init__(self):
		super(BetweenConstraint, self).__init__()

	def name(self):
		return "between"

	def validate(self, value, constraint_value, field_name, doc):
		min = constraint_value[0]
		max = constraint_value[1]

		if isinstance(value, numbers.Number):
			if value < min or value > max:
				return {"min" : min, "max" : max}
		elif isinstance(value, str) or isinstance(value, list) or isinstance(value, dict):
			if len(value) < min or len(value) > max:
				return {"min" : min, "max" : max}
		return True	

class SizeConstraint(Constraint):

	def __init__(self):
		super(SizeConstraint, self).__init__()

	def name(self):
		return "size"

	def validate(self, value, constraint_value, field_name, doc):
		if isinstance(value, numbers.Number) and value != constraint_value:
			return {"size" : constraint_value}
		elif isinstance(value, str) and len(value) != constraint_value:
			return {"size" : constraint_value}
		elif isinstance(value, list) and len(value) != constraint_value:
			return {"size" : constraint_value}
		return True

class FormatConstraint(Constraint):

	def __init__(self):
		super(FormatConstraint, self).__init__()

	def name(self):
		return "data_format"

	def validate(self, value, constraint_value, field_name, doc):

		if isinstance(value, str):

			#FIX ME HER
			if constraint_value == "email" and not is_email(value):
				return {"data_format" : constraint_value}
			elif constraint_value == "ip" and not is_ip(value):
				return {"data_format" : constraint_value}
			elif constraint_value == "mac" and not is_mac(value):
				return {"data_format" : constraint_value}

			return True

		return {"data_format" : constraint_value}	
		
		



#This one lets you pass function as a constraint_value
class ValidatorConstraint(Constraint):

	def __init__(self):
		super(ValidatorConstraint, self).__init__()
		
	def name(self):
		return "validator"

	def validate(self, value, constraint_value, field_name, doc):
		success = bool(constraint_value['function'](value))
		if not success:
			if "message" in constraint_value:
				return {"message" : constraint_value["message"]}
			return False
		return True

class RegexConstraint(Constraint):

	def __init__(self):
		super(RegexConstraint, self).__init__()

	def name(self):
		return "regex"

	def validate(self, value, constraint_value, field_name, doc):
		reg = re.compile(constraint_value)
		if value != None:
			success = (reg.match(value) != None)
			if success:
				return True
			else:
				return {"regex" : constraint_value} 
		return {"regex" : constraint_value} 


class CoerceConstraint(Constraint):

	def __init__(self):
		super(CoerceConstraint, self).__init__()

	def name(self):
		return "coerce"

	def validate(self, value, constraint_value, field_name, doc):
		if hasattr(constraint_value, '__call__'):
			try:
				doc[field_name] = constraint_value(value)
				return True		
			except:
				return False
		raise ConstrainException("Coerce must be callable.")
