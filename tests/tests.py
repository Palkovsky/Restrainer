import unittest
from restrainer import Validator

'''
	you have to look harder, it's actually pretty easy to read when you step on it
	you should only know that validate methods returns list of errors
'''
class ValidatorTest(unittest.TestCase):

	def setUp(self):
		self.validator = Validator()

	def test_type_constraint(self):
		rules = {"field" : {"type" : "integer"}}

		self.validator.validate({"field" : ""}, rules = rules)
		self.assertTrue(self.validator.fails())

		self.validator.validate({"field" : 2}, rules = rules)
		self.assertFalse(self.validator.fails())

	def test_list_type_constraint(self):
		rules = {"field" : {"list_type" : "string"}}

		self.validator.validate({"field" : [1, "foo", 3]}, rules = rules)
		self.assertTrue(self.validator.fails())

		self.validator.validate({"field" : [1.2, 3]}, rules = rules)
		self.assertTrue(self.validator.fails())

		self.validator.validate({"field" : [1, 2, 8]}, rules = rules)
		self.assertTrue(self.validator.fails())

		self.validator.validate({"field" : ["f", "o", "o"]}, rules = rules)
		self.assertFalse(self.validator.fails())

	def test_required_constraint(self):
		rules = {"field" : {"required" : True}, "field_2" : {"required" : True}}

		self.assertEqual(len(self.validator.validate({"field" : "foo", "field_2" : "bar"}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : "foo", "field_3" : "bar"}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())	

		self.assertEqual(len(self.validator.validate({}, rules = rules)), 2)
		self.assertTrue(self.validator.fails())	

	def test_min_constraint(self):
		rules = {"field" : {"min" : 12.5}}

		self.assertEqual(len(self.validator.validate({"field" : 12.5}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 14}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())	

		self.assertEqual(len(self.validator.validate({"field" : "aaaaaaaaaaaaaaaaaaaaaaaaaaa"}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 11.2}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : "aaa"}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

	def test_max_constraint(self):
		rules = {"field" : {"max" : 12.5}}

		self.assertEqual(len(self.validator.validate({"field" : 12.5}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 14}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : "aaaaaaaaaaaaaaaaaaaaaaaaaaa"}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 11.2}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : "aaa"}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

	def test_between_constraint(self):
		rules = {"field" : {"between" : [5, 10]}}

		self.assertEqual(len(self.validator.validate({"field" : 5}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 10}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 6.4}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 2.2}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : "12345678901"}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

	def test_value_constraint(self):
		rules = {"field" : {"value" : [56, "text", 2.4]}}

		self.assertEqual(len(self.validator.validate({"field" : "tex"}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : "text"}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 56}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 2.4}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

	def test_size_constraint(self):
		rules = {"field" : {"size" : 4}}

		self.assertEqual(len(self.validator.validate({"field" : "text"}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : [1, 2, 3, 4]}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 4}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : [1, 2, 3]}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : "tex"}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

	def test_regex_constraint(self):
		rules = {"field" : {"regex" : r'a+'}}

		self.assertEqual(len(self.validator.validate({"field" : "ab"}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : "abcda"}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : "cda"}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

	def test_validator_constraint(self):
		is_even = lambda x: (x%2 == 0)

		rules = {"field" : {"validator" : {"function" : is_even, "message" : "must be odd"}}}

		self.assertEqual(len(self.validator.validate({"field" : 3}, rules = rules)), 1)
		self.assertTrue(self.validator.fails())

		self.assertEqual(len(self.validator.validate({"field" : 2}, rules = rules)), 0)
		self.assertFalse(self.validator.fails())

	def test_coerce_constraint(self):
		divide_by_two = lambda x: x/2

		rules = {"field" : {"coerce" : divide_by_two}}
		document = {"field" : 7}

		self.validator.validate(document, rules = rules)

		self.assertEqual(document["field"], 3.5)

	def test_nested_dicts(self):

		rules = {
			"field" : {
				"type" : "object",
				"required" : True,
				"properties" : {
					"field_2" : {
						"type" : "object",
						"properties" : {
							"lvl_3_field" : {"required" : True}
						}
					},
					"lvl_2_field" : {"required" : True}
				}
			},
			"lvl_1_field" : {"required" : True}
		}

		doc = {
			"lvl_1_field" : "content",
			"field" : {
				"lvl_2_field" : "content",
				"field_2" : {
					"lvl_3_field" : "content"
				}
			}
		}

		self.validator.validate(doc, rules=rules)
		self.assertEqual(len(self.validator.errors()), 1)
		self.assertEqual(len(self.validator.errors()[0]['field']), 1)
		self.assertEqual(len(self.validator.errors()[0]['field'][0]['field_2']), 0)
		self.assertFalse(self.validator.fails())

		doc = {
			"lvl_1_field" : "content",
			"field" : {
				"lvl_2_field" : "content",
				"field_2" : {
				}
			}
		}

		self.validator.validate(doc, rules=rules)
		self.assertEqual(len(self.validator.errors()), 1)
		self.assertEqual(len(self.validator.errors()[0]['field']), 1)
		self.assertEqual(len(self.validator.errors()[0]['field'][0]['field_2']), 1)
		self.assertTrue(self.validator.fails())

	def test_nested_dict_lists(self):
		rules = {
		    "name" : {
		        "type" : "string",
		        "size" : 10, #Size in case of string means its length
		        "required" : True
		    },
		    "pets" : {
		        "required" : True,
		        "type" : "list",
		        "items" : {
		            "name" : {"type" : "string", "required" : True},
		            "age" : {"min" : 0, "max" : 100}
		        }
		    }
		}
		
		doc =  {
			"name" : "Jerry",
			"pets" : [
				{"name" : "Dog 1", "age" : 101},
				{"name" : "Dog 2", "age" : 4},
				{"name" : "Dog 3", "age" : 4},
				{"age" : 32}
			]
		}

		self.validator.validate(doc, rules=rules)
		self.assertEqual(len(self.validator.errors()), 2) #one for name not matching size/one for pets nested list
		self.assertEqual(bool("pets" in self.validator.errors()[0] or "pets" in self.validator.errors()[1]), True)
		self.assertTrue(self.validator.fails())
