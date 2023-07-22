from functools import wraps
from src import env_configuration, app_configuration
from src.utils.gen_credential_data import gen_data
from src.utils.file_helper import write_to_json
from src.utils.api_logger import ApiLogger
from src.data_layer.sp_dao import SPDao
from src.auth.auth import Auth


def init_credential_json():
    ApiLogger.log_debug("Creating credential json file.")

    write_to_json(
        json_string=gen_data(env_configuration=env_configuration),
        out_file_path="credentials.json",
    )


def create_ftsi():
    SPDao.call_sp(app_configuration.api_config.index_sp_name)


def check_ftsi(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        create_ftsi()
        return func(*args, **kwargs)

    return wrapper


def start_auth():
    auth = Auth()
    auth.start()


def validate_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_auth()
        return func(*args, **kwargs)

    return wrapper
