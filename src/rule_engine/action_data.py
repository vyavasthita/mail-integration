from dataclasses import dataclass
from enum import Enum, IntEnum


class ActionCode(IntEnum):
    MOVE = 1
    READ_UNREAD = 2
    

@dataclass
class ActionData:
    code: int = None
    destination: str = None

