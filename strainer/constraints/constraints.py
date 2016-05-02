import numbers
from abc import ABCMeta, abstractmethod, abstractproperty
from .utils import is_email

class Constraint(metaclass=ABCMeta):

	'''
		Name is how your constraint will be called in rules tree.
		So for min constraint it may be 'min' or 'minimum'
	'''
	def __init__(self):
		pass

	@abstractproperty
	def name(self):
		pass

	'''
		If you don't wanna pass additional key,values you can return basically everything.
		But it's important that if validation is failed expressions logical value shuld be False, if succeded - True

		If you wanna pass additional arguments when it failed, it should look like that:
		{
			"validation" : False,
			**kwargs - for additional args
		}

		value - value of doc field
		constraint_value - value declared in constraints definition
	'''
	@abstractmethod
	def validate(self, value, constraint_value):
		pass


class ExsitanceConstraint(Constraint):

	def __init__(self):
		super(Constraint, self).__init__()

	def name(self):
		return "required"

	def validate(self, value, constraint_value):
		return value != None

class TypeConstraint(Constraint):

	def __init__(self):
		super(TypeConstraint, self).__init__()

	def name(self):
		return "type"

	def validate(self, value, constraint_value):
		if constraint_value == "numeric" and not isinstance(value, numbers.Number):
			return {"type" : "numeric"}
		elif constraint_value == "string" and not isinstance(value, str):
			return {"type" : "string"}
		elif constraint_value == "boolean" and not isinstance(value, bool):
			return {"type" : "boolean"}
		elif constraint_value == "list" and not isinstance(value, list):
			return {"type" : "list"}
		elif constraint_value == "object" and not isinstance(value, dict):
			return {"type" : "object"}
		return True

class ValueConstraint(Constraint):

	def __init__(self):
		super(ValueConstraint, self).__init__()
	
	def name(self):
		return "value"

	def validate(self, value, constraint_value):
		if not value in constraint_value:
			return {"allowed" : constraint_value}
		return True
		
class MinConstraint(Constraint):

	def __init__(self):
		super(MinConstraint, self).__init__()

	def name(self):
		return "min"

	def validate(self, value, constraint_value):
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

	def validate(self, value, constraint_value):
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

	def validate(self, value, constraint_value):
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

	def validate(self, value, constraint_value):
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

	def validate(self, value, constraint_value):
		if constraint_value == "email" and not is_email(value):
			return {"data_format" : "email"}
		return True	
		
		