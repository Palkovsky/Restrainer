import numbers
from .constraints.constraints import *
from .constraints.exceptions import *

class Validator(object):

	def __init__(self, rules, constrainers = []):
		self.__errors = []
		self.__errors_count = 0
		self.__rules = rules
		if len(constrainers) == 0:
			self.__constrainers = self.__default_constrains()
		else:
			self.__constrainers = constrainers
		self.__build_method = self.__build_error

	def __default_constrains(self):
		return [ExsitanceConstraint(), TypeConstraint(), ValueConstraint(),
		 		MinConstraint(), MaxConstraint(), BetweenConstraint(),
		 		SizeConstraint(), FormatConstraint(), ListTypeConstraint(),
		 		ValidatorConstraint(), RegexConstraint(), CoerceConstraint()]

	def __find_constrainer(self, name):
		for constrainer in self.__constrainers:
			if name == constrainer.name():
				return constrainer
		return None

	def set_build_method(self, method):
		self.__build_method = method

	def load_constraint(self, constraint):
		if isinstance(constraint, Constraint):
			self.__constrainers.append(constraint)

	def fails(self):
		return self.__errors_count > 0

	def errors(self):
		return self.__errors

	def validate(self, doc = {}, rules = None):
		if rules == None:
			rules = self.__rules
		self.__errors_count = 0
		self.__errors = []
		self.__errors += self.__validate_rules(doc, rules = rules)
		return self.__errors

	def __validate_rules(self, doc, rules = None, index = None):

		errors = []


		for field_name, constraints in rules.items():

			data_value = doc.get(field_name, None)

			for constraint, constraint_value in constraints.items():

				if constraint == "items":

					if data_value == None or not isinstance(data_value, list):
						continue

					errors_collection = {field_name : []}
					for index, item in enumerate(data_value):
						errors_collection[field_name] += self.__validate_rules(item, rules = constraint_value, index = index)
					errors.append(errors_collection)

				elif constraint == "properties":

					if data_value == None or not isinstance(data_value, dict):
						continue

					target_errors = self.__validate_rules(data_value, rules = constraint_value)
					errors.append({ field_name :  target_errors })
				
				else:

					constrainer = self.__find_constrainer(constraint)
					if constrainer == None:
						raise ConstrainException("No constrainer found for attribute: '" + constraint + "'.")

					if (constrainer.accept_null or (data_value != None and not constrainer.accept_null)):
						validation_result = constrainer.validate(data_value, constraint_value, field_name, doc)
						succeeded = bool(validation_result) and not isinstance(validation_result, dict)

						if not succeeded:
							if isinstance(validation_result, dict):
								if index != None:
									errors.append(self.__build_method(field_name, constraint, index = index, **validation_result))
								else:
									errors.append(self.__build_method(field_name, constraint, **validation_result))
							else:
								if index != None:
									errors.append(self.__build_method(field_name, constraint, index = index))
								else:
									errors.append(self.__build_method(field_name, constraint))
							self.__errors_count += 1

		return errors

	def __build_error(self, field_name, constraint, **kwargs):
		error = {"field" : field_name, "constraint" : constraint}
		for key, value in kwargs.items():
			error[key] = value
		return error

'''
PERSONAL THOUGHTS DON'T READ

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

	{
		"age" : {
			"type" : "numeric",
			"required" : True
		}, 
		"participants" : {
			"type" : "list",
			"items" : {
				"name" : {
					"type" : "string",
					"required" : True
				},
				"parties" : {
					"type" : "list",
					"items" : {
						"name" : {
							"required" : True,
							"type" : "string"
						},
						"support" : {
							"type" : "numeric"
						}
					}
				}
			}
		}
	}

	[
		{
			"field" : "participants",
			"items" : [
				{
					"index" : 2
					"field" : "name",
					"constraint" : "type",
					"type" : "string"
				}
			]
		}
	]

	Types:
		-numeric
		-string
		-object
		-boolean
		-object
		-list(for primitves)
		-object_list(for objects)
'''