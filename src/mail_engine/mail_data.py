from dataclasses import dataclass, field


@dataclass
class MailData:
    query_string: str
    query_data: list = field(default_factory=list)
