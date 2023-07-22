from src import env_configuration
from src.utils.gen_credential_data import gen_data
from src.utils.file_helper import write_to_json
from src.utils.api_logger import ApiLogger

def init_credential_json():
    ApiLogger.log_debug("Creating credential json file.")

    write_to_json(
        json_string=gen_data(env_configuration=env_configuration),
        out_file_path="credentials.json",
    )
