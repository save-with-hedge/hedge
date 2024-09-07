import json


def read_json(filepath):
    """
    :param filepath: location of json file containing data
    """
    with open(filepath) as f:
        data = json.load(f)
    return data


def write_json(filepath, json_data):
    """
    :param filepath: output file to write to
    :param json_data: python dictionary containing data to be written
    """
    data = json.dumps(json_data, indent=2)
    with open(filepath, "w") as f:
        f.write(data)
