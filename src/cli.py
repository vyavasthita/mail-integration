import argparse
from enum import IntEnum
from dataclasses import dataclass


class ArgOption(IntEnum):
    FETCH_EMAIL = 1
    SHOW_RULES = 2
    APPLY_RULES = 3


@dataclass
class Choice:
    option: ArgOption = 1
    rule: str = None


parser = argparse.ArgumentParser(
    description="List the cmd parameters for gmail api",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)


def read_arguments(available_rules: list):
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-e",
        "--emails",
        default=False,
        action="store_true",
        help="To fetch emails from Gmail",
    )
    group.add_argument(
        "-s", "--showrules", action="store_true", help="To show all the available rules"
    )

    group.add_argument(
        "-a",
        "--applyrule",
        choices=available_rules,
        help="Apply given rule by its name with value from json key 'rule'",
        nargs=1,
        type=str,
    )


def get_choice(available_rules: list) -> Choice:
    read_arguments(available_rules=available_rules)

    choice = Choice()
    args = parser.parse_args()

    if args.emails:
        choice.option = ArgOption.FETCH_EMAIL
    elif args.showrules:
        choice.option = ArgOption.SHOW_RULES
    else:
        choice.option = ArgOption.APPLY_RULES
        choice.rule = args.applyrule[0]

    return choice
