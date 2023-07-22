from dataclasses import dataclass
from enum import Enum, IntEnum


class ActionCode(IntEnum):
    MOVE = 1
    READ = 2
    UNREAD = 3


@dataclass
class ActionData:
    code: int = None
    label: str = None
