import os
import json
from dataclasses import dataclass


@dataclass
class JsonReader:
    file_path: str
    data: dict = None

    def read(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path) as json_file_object:
                    self.data = json.load(json_file_object)
            except ValueError as error:
                print(f"Invalid Json File. {self.file_path}")
        else:
            raise ValueError(
                "Connection configuration file path '{}' is invalid.".format(
                    self.file_path
                )
            )
        return self.data
