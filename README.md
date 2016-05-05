# Restrainer
Allows you to easily validate your Python dictionaries. It provides easily parsable response, so I found it very fitting in REST APIs. You can also easily extend it to fit your needs, for example if  you'd want to check uniqueness.
 
## Instalation
It's compatible with Python 3.+

    sudo pip install restrainer
 
## Examples

Let's say we're handling user creation in REST API. Below is sample rules set.
    
    {
        "username" : {
            "required" : True,
            "type" : "string",
            "between" : [3, 20]
        },
        "email" : {
            "required" : True,
            "type" : "string",
            "data_format" : "email"
        },
        "password" : {
            "required" : True,
            "type" : "string",
            "min" : 7
         }
    }

Putting it in front of this object:

    {
        "username" : "as",
        "email" : "sexsexsex"
    }
    
will result with:

    [
        {
            "field": "password",
            "constraint": "required"
        },
        {
            "min": 3,
            "max": 20,
            "field": "username",
            "constraint": "between"
        },
        {
            "field": "email",
            "data_format": "email",
            "constraint": "data_format"
        }
    ]
    
### How to use it?

    from restrainer import Validator
    
    rules = {
        "username" : {
            "required" : True,
            "type" : "string",
            "between" : [3, 20]
        },
        "email" : {
            "required" : True,
            "type" : "string",
            "data_format" : "email"
        },
        "password" : {
            "required" : True,
            "type" : "string",
            "min" : 7
         }
    }
    
    data = {
        "username" : "as",
        "email" : "sexsexsex"
    }
    
    validator = Validator(rules)
    validator.validate(data) #This also returns errors list
    
    if validator.fails():
        print(validator.errors())
    else:
        print("VALIDATION SUCCESSFUL")
        
## Nested lists/dicts
    
Sometimes you may want to have nested lists or dictionaries in your data set and validate them.

### Nested dict

If you wanna have nested dict and validate it you can use 'properties' attribute:

    rules = {
        "name" : {
            "type" : "string",
            "size" : 10, #Size in case of string means its length
            "required" : True
        },
        "pet" : {
            "required" : True,
            "type" : "object",
            "properties" : {
                "name" : {"type" : "string", "required" : True},
                "age" : {"min" : 0, "max" : 100}
            }
        }
    }
    
    data = {
        "name" : "Batman",
        "pet" : {
        	"name" : "Rex",
        	"age" : 200
        }
    }
    
Validating it will reslut with:

    [
        {
            "field": "name",
            "constraint": "size",
            "size": 10
        },
        {
            "pet": [
                {
                    "field": "age",
                    "constraint": "max",
                    "max": 100
                }
            ]
        }
    ]

### List of dicts

Simiral to nested dict, but this time you should use 'items' keyword.

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
    
    data =  [
        {
            "pets": [
                {
                    "index": 0,
                    "field": "age",
                    "constraint": "max",
                    "max": 100
                },
                {
                    "index": 2,
                    "field": "name",
                    "constraint": "required"
                }
            ]
        },
        {
            "size": 10,
            "index": 2,
            "field": "name",
            "constraint": "size"
        }
    ]
    
Responds with:

    [
        {
            "pets": [
                {
                    "index": 0,
                    "field": "age",
                    "constraint": "max",
                    "max": 100
                },
                {
                    "index": 2,
                    "field": "name",
                    "constraint": "required"
                }
            ]
        },
        {
            "size": 10,
            "index": 2,
            "field": "name",
            "constraint": "size"
        }
    ]

### List of primitives

This is need a little bit more work on creating new constraints. Currently you can only validate type of items in array of primitives(numeric, string, integer, boolean etc.). You do it like that:

    "ids" : {
        "type" : "list",
        "list_type" : "integer"
    } 
    
## Built-in constrainers

Name | Accepted Values
----- | -------------
type | string
list_type | string
required | boolean
value | array ex. ["male", "female"]
min | numeric
max | numeric
between | array of 2 numeric ex. [2, 10]
size | integer
data_format | string - email/mac/ip
regex | string - regular expression
validator | dictionary - {"function": f, "message" : "error msg"} 
coerce | callable

### Validator constrainer

Allows you to pass function which shall return True/False and accept one argument. This argument will be data passed by user. And if you return False validation will fail.

### Coerce constrainer

Coerce function should take one argument and return some value. Let's say you accept numeric and if you pass coerce function divide_by_two, final version in document will be changed to initial value divided by two.


## Custom constrainers

Shall be written soon.