import os
from src import env_configuration, environment
from src.rule_parser import RuleParser
from utils.gen_credential_data import gen_data
from utils.file_helper import write_to_json


def init_rule_parser():
    rule_parser_file_path = os.path.join(
        os.getcwd(), "config", environment, "email_rules.json"
    )

    # parse rule parser
    parser = RuleParser(file_path=rule_parser_file_path)
    data = parser.parse()


def init_credential_json():
    write_to_json(
        json_string=gen_data(env_configuration=env_configuration),
        out_file_path="credentials.json",
    )
