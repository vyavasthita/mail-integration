import os
from src.env_config import config_by_name

environment = os.getenv("BUILD_ENV") or "development"

env_configuration = config_by_name[environment]
