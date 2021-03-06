import numbers
from restrainer.constraints.constraints import *
from restrainer.constraints.exceptions import *

class Validator(object):

	def __init__(self, rules = {}, constrainers = []):
		self.__errors = []
		self.__errors_count = 0
		self.__rules = rules
		self.__constrainers = []

		if len(constrainers) == 0:
			for default_constraint in self.__default_constrains():
				self.load_constraint(default_constraint)
		else:
			for constrainer in constrainers:
				self.load_constraint(constrainer)

		self.__type_constraint = TypeConstraint()
		self.__build_method = self.__build_error

	def __default_constrains(self):
		return [ExsitanceConstraint(), ValueConstraint(),
		 		MinConstraint(), MaxConstraint(), BetweenConstraint(),
		 		SizeConstraint(), FormatConstraint(), ListTypeConstraint(),
		 		ValidatorConstraint(), RegexConstraint(), CoerceConstraint()]

	def __find_constrainer(self, name):
		for constrainer in self.constraints():
			if name == constrainer.name():
				return constrainer
		return None

	def set_type_constraint(self, type_constraint):
		self.__type_constraint = type_constraint

	def register_type(self, name, cls):
		self.__type_constraint.register_type(name, cls)

	def set_build_method(self, method):
		self.__build_method = method

	def constraints(self):
		return self.__constrainers + [self.__type_constraint]

	def load_constraint(self, constraint):
		if isinstance(constraint, Constraint):
			for constrainer in self.__constrainers:
				if constraint.name() == constrainer.name():
					raise ConstrainException("Constrainer with name'" + constraint.name() + "'already registered.")
			self.__constrainers.append(constraint)

	def fails(self):
		return self.__errors_count > 0

	def errors(self):
		return self.__errors

	def validate(self, doc, rules = None):
		if rules == None:
			rules = self.__rules
		self.__errors_count = 0
		self.__errors = []
		self.__errors += self.__validate_rules(doc, rules = rules)
		return self.__errors

	def __validate_rules(self, doc, rules = {}, index = None):

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