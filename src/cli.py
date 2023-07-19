import argparse
from dataclasses import dataclass


parser = argparse.ArgumentParser(
    description="List the rules for gmail api",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

# parser.add_argument("-r", "--rules", action="store_true")
parser.add_argument(
    "--emails", default=False, action="store_true", help="To fetch emails from Gmail"
)


@dataclass
class Choice:
    emails: bool = False


def get_choice() -> Choice:
    choice = Choice()

    args = parser.parse_args()

    choice.emails = args.emails

    return choice


def get_rule():
    return parser.get_rule("rule_1")
