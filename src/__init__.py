import os
from src.config.env_config import config_by_name
from src.config.app_config import AppConfigParser


environment = os.getenv("BUILD_ENV") or "development"


def create_log_directory():
    base_dir = os.path.abspath(os.path.dirname(__name__))

    if not os.path.exists(os.path.join(base_dir, env_configuration.LOGS_DIR)):
        os.mkdir(os.path.join(base_dir, env_configuration.LOGS_DIR))


app_config_file_path = os.path.join(
    os.getcwd(), "config", environment, "app_config.json"
)

env_configuration = config_by_name[environment]

app_config_parser = AppConfigParser(file_path=app_config_file_path)

app_configuration = app_config_parser.parse()
