import json


def write_json(filename, json_data):
    data = json.dumps(json_data, indent=2)
    with open(filename, "w") as f:
        f.write(data)
