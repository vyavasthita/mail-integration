import argparse
from rule_parser import JsonRuleParser


parser = argparse.ArgumentParser(description="List the rules for gmail api")


parser.add_argument("-r", "--rules", action="store_true")

args = parser.parse_args()

parser = JsonRuleParser()


def get_rule():
    return parser.get_rule("rule_1")
