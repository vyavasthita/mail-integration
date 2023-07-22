import json
import os


def write_to_file(data, out_file_path):
    with open(out_file_path, "w") as token:
        token.write(data)


def write_to_json(json_string, out_file_path):
    with open(out_file_path, "w") as outfile:
        json.dump(json_string, outfile, indent=4)


def delete_file(file_path):
    # If file exists, delete it.
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        # If it fails, inform the user.
        print(f"Failed to delete {file_path}. File does not exist.")

def check_file_exists(file_path):
    return os.path.exists(file_path)