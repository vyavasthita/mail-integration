from src import configuration
from utils.gen_credential_data import gen_data


out_json_file_path = "credentials.json"
json_string = gen_data(configuration=configuration)
