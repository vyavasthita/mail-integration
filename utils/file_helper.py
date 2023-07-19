import json


def write_to_file(data, out_file_path):
    with open(out_file_path, "w") as token:
        token.write(data)


def write_to_json(json_string, out_file_path):
    with open(out_file_path, "w") as outfile:
        json.dump(json_string, outfile, indent=4)
