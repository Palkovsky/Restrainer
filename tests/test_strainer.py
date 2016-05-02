import unittest
#Don't forget to add parent directory to $path
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

rules = {
	"name" : {
		"type" : "string",
		"required" : True
	},
	"age" : {
		"type" : "numeric",
		"between" : [0, 100]
	},
	"numery" : {
		"type" : "list",
		"list_type" : ["string", "numeric"]
	}
}

data = {
	"name" : "Ryszard Petru",
	"age" : 30,
	"numery" : [1, 10, {}, "tekst"]
}

validator = Validator(rules)
pprint(validator.validate(data))