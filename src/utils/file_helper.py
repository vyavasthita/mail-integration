"""Helper module to perform file related operations.

@file file_helper.py
@author Dilip Kumar Sharma
@date 19 July 2023

About; -
--------
    Helper module to perform file related operations.
    Eg. Delete file, write to file.
"""

# Core python packages
import json
import os


def write_to_file(data: str, out_file_path: str) -> None:
    """Write data to file

    Args:
        data (str): data to write
        out_file_path (str): File to write data to
    """
    with open(out_file_path, "w") as token:
        token.write(data)


def write_to_json(json_string: dict, out_file_path: str) -> None:
    """Write json data to file

    Args:
        json_string (dict): dict to write to
        out_file_path (str): File to write data to
    """
    with open(out_file_path, "w") as outfile:
        json.dump(json_string, outfile, indent=4)


def delete_file(file_path: str) -> None:
    """Delete file if exists

    Args:
        file_path (str): file to delete
    """
    # If file exists, delete it.
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        # If it fails, inform the user.
        print(f"Failed to delete {file_path}. File does not exist.")


def check_file_exists(file_path: str) -> None:
    """Check if file exists

    Args:
        file_path (str): File to check

    Returns:
        None:
    """
    return os.path.exists(file_path)
