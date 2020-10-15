import json
import os


person = {
    "Name": "Matthieu",
    "Age": 28,
    "Height": 1.93,
    "Born": "La Rochelle",
    "Favourite Music": "Hiphop",
}

json_file = os.path.join(os.path.dirname(__file__), "json_file_test.json")

with open(json_file, "w") as out_json:
    json.dump(person, out_json, indent=4)

with open(json_file, "r") as f:
    json_data = json.load(f)

print(json_data)