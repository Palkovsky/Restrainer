import unittest, json, datetime
#Don't forget to add parent directory to $path
#export PYTHONPATH=${PYTHONPATH}:~/Desktop/python/strainer
from restrainer import Validator
from restrainer import TypeConstraint
from pprint import pprint

'''
rules = {
			"age" : {
				"type" : "numeric",
				"required" : True
		}, 
		"party" : {
			"type" : "object",
			"properties" : {
				"name" : {
					"type" : "string",
					"between" : [5, 15],
					"required" : True
				},
				"support" : {
					"type" : "numeric",
					"min" : 10,
					"max" : 50
				},
				"sponsors" : {
					"type" : "list",
					"required" : True,
					"min" : 2,
					"items" : {
						"name" : {
							"type" : "string",
							"required" : True
						},
						"ile" : {
							"type" : "numeric",
							"between" : [0, 10000],
							"required" : True
						}
					}
				}
			}
		}
	}
'''

def is_odd(num):
	return (num % 2 != 0)

def divide_by_two(value):
	return value / 2

rules = {
	"age" : {
		"type" : "numeric",
		"required" : True
	},
	"name" : {
		"type" : "string",
		"required" : True,
		"data_format" : "mac"
	},
	"gender" : {
		"required" : True,
		"value" : ["male", "female"]
	},
	"party" : {
		"type" : "object",
		"required" : True,
		"properties" : {
			"name" : {
				"type" : "string",
				"between" : [1, 10]
			},
			"sponsors" : {
				"type" : "list",
				"required" : True,
				"min" : 2,
				"items" : {
					"name" : {
						"type" : "string",
						"required" : True
					},
					"ile" : {
						"type" : "numeric",
						"between" : [0, 10000],
						"required" : True
					}
				}
			}	
		}
	}
}

data = {
	"age" : 11.3,
	"name" : "00:29:15:80:4E:4A",
	"gender" : "male",
	"party" : {
		"name" : "Platforma",
		"sponsors" : [
			{
				"name" : "Ryszard Petru",
				"ile" : 10
			},
			{
				"name" : "Ryszard Kalisz",
				"ile" : 123
			}
		]
	}
}

validator = Validator(rules)
validator.register_type("datetime", datetime.datetime)
validator.validate(data)

try:
	print(json.dumps(data, indent=4))
except TypeError:
	pprint(data)

if validator.fails():
	print("Validation FAILED")
else:
	print("Validation SUCCESS")

try:
	print(json.dumps(validator.errors(), indent=4))
except TypeError:
	pprint(validator.errors())
