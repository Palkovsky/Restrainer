import numbers
from .constraints.constraints import *
from .exceptions import *

class Validator(object):

	def __init__(self, rules):
		self.__errors = []
		self.__rules = rules
		self.__constrainers = self.__default_constrains()

	def __default_constrains(self):
		return [ExsitanceConstraint(), TypeConstraint(), ValueConstraint(),
		 		MinConstraint(), MaxConstraint(), BetweenConstraint(),
		 		SizeConstraint(), FormatConstraint()]

	def __find_constrainer(self, name):
		for constrainer in self.__constrainers:
			if name == constrainer.name():
				return constrainer
		return None

	def load_constraint(self, constraint):
		if isinstance(constraint, Constraint):
			self.__constrainers.append(constraint)

	def fails(self):
		return (len(self.errors) > 0)

	def errors(self):
		return self.__errors

	def validate(self, doc = {}):
		self.__errors = []

		for field_name, constraints in self.__rules.items():

			data_value = doc.get(field_name, None)

			for constraint, constraint_value in constraints.items():
				constrainer = self.__find_constrainer(constraint)

				if constrainer == None:
					raise ConstraintException("No constrainer found for attribute: '" + constraint + "'.")

				validation_result = constrainer.validate(data_value, constraint_value)
				succeeded = bool(validation_result) and not isinstance(validation_result, dict)

				if not succeeded:
					if isinstance(validation_result, dict):
						self.__errors.append(self.__build_error(field_name, constraint, **validation_result))
					else:
						self.__errors.append(self.__build_error(field_name, constraint))

		return self.__errors

	def __build_error(self, field_name, constraint, **kwargs):
		error = {"field" : field_name, "constraint" : constraint}
		for key, value in kwargs.items():
			error[key] = value
		return error

'''
	Example rules set:
		//Will go with this one
		{
			"field_1" : {
				"type" : "string",
				"max" : 20,
				"data_format" : "email",
				"required" : True
			},
			"field_2" : {
				"type" : "numeric",
				"between" : [1, 100]
			}
		}
	

	VS

	{
		"field_1" : ["type:string|max:20|data_format:email|required:True"],
		"field_2" : ["type:numeric|between:1:100"]
	}

	Example evaluated object:
	{"field_1" : "abcdefghijklmnouprstwvxz"}
'''