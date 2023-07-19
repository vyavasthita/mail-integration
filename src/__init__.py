import os
from src.env_config import config_by_name
from src.app_config import AppConfigParser


environment = os.getenv("BUILD_ENV") or "development"

env_configuration = config_by_name[environment]


app_config_file_path = os.path.join(
    os.getcwd(), "config", environment, "msg_config.json"
)

app_config_parser = AppConfigParser(file_path=app_config_file_path)

app_configuration = app_config_parser.parse()

