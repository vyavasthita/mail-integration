"""To read json file.

@file json_reader.py
@author Dilip Kumar Sharma
@date 21 July 2023

About; -
--------
    Read json file and returns complete json object.
"""
# Core python packages
import os
import json
from dataclasses import dataclass

# Application packages
from src.utils.api_logger import ApiLogger


@dataclass
class JsonReader:
    file_path: str

    def read(self) -> dict:
        """Reads Json file

        Raises:
            ValueError: If invalid json

        Returns:
            dict: Whole json data
        """
        data = None
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path) as json_file_object:
                    data = json.load(json_file_object)
            except ValueError:
                ApiLogger.log_error(f"Invalid Json File. {self.file_path}")
        else:
            raise ValueError(
                "Connection configuration file path '{}' is invalid.".format(
                    self.file_path
                )
            )
        return data
