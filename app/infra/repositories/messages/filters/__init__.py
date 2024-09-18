from dataclasses import dataclass


@dataclass
class GetMessagesFilter:
    limit: int = 10
    offset: int = 0
