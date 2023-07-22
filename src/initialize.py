import os
from src import env_configuration, environment
from src.rule_engine.rule_parser import RuleParser
from src.utils.gen_credential_data import gen_data
from src.utils.file_helper import write_to_json
from src.utils.api_logger import ApiLogger


def init_rule_parser():
    ApiLogger.log_debug("Reading rule parsing json configuration.")

    rule_parser_file_path = os.path.join(
        os.getcwd(), "config", environment, "email_rules.json"
    )

    # parse rule parser
    parser = RuleParser(file_path=rule_parser_file_path)
    return parser.parse()


def init_credential_json():
    ApiLogger.log_debug("Creating credential json file.")

    write_to_json(
        json_string=gen_data(env_configuration=env_configuration),
        out_file_path="credentials.json",
    )
