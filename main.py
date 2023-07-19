from src import configuration
from utils.gen_credential_data import gen_data
from utils.file_helper import write_to_json

out_json_file_path = "credentials.json"
json_string = gen_data(configuration=configuration)


write_to_json(
    json_string=gen_data(configuration=configuration),
    out_file_path=out_json_file_path,
)