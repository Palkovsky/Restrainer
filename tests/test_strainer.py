import unittest, json
#Don't forget to add parent directory to $path
#export PYTHONPATH=${PYTHONPATH}:~/Desktop/python/strainer
from strainer import Validator
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

rules = {
	"age" : {
		"type" : "numeric",
		"required" : True,
		"validator" : {"function" : is_odd, "message" : "must be odd number"}
	},
	"name" : {
		"type" : "string",
		"required" : True,
		"regex" : "[a-z]+"
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
	"age" : 11,
	"name" : "A",
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
#pprint(validator.validate(data))
print(json.dumps(validator.validate(data), indent=4))