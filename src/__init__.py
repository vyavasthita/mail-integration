import os
from src.config import config_by_name

environment = os.getenv("BUILD_ENV") or "development"

configuration = config_by_name[environment]
