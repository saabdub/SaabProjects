import FavouriteRecursion as f

json_data = {
    "FirstName": "John",
    "LastName": "Smith",
    "Address": {
        "Street": "123 Main Street",
        "City": "Anytown",
        "State": "NY",
        "Zip": "12345",
        "Question1": ["yes", "no", "maybe"],
    },
    "Question2": "yes",
    "Question3": {"A": "11",
                  "B": 12,
                  "C": 13},
    "Question4": ["asda", {"Question1": "1"}, {"Question2": "2", "Question3": "3"}, "maybe"],
    "Question5": {"A": "11",
                  "B": 12,
                  "C": {
                        "D": "13",
                        "E": "14",
                        "F": ["1", "2", "3"]
                  }},
}

data = f.flattening(json_data)

assert data["Question3.C"] == 13
assert data["Question4.1.Question1"] == "1"
assert data["Question5.C.F"] == ['1', '2', '3']

json_data2 = {"FirstName": "John",
    "LastName": "Smith",
    "Address": {
        "Street": "123 Main Street",
        "City": "",
        "State": "",
        "Zip": "",
        "Question1": []},
    "Question2": {}
    }

data = f.flattening(json_data2)

assert data["Question2"] == ""
assert data["FirstName"] == "John"
assert data["Address.Question1"] == ""


json_data3 = {}
data = f.flattening(json_data3)
assert data is None







#for key, value in data.items():
#    print(key, " = ", value)


