from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.events.base import BaseEvent


@dataclass(eq=False)
class BaseEntity(ABC):
    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    created_at: datetime = field(
        default_factory=datetime.now, kw_only=True
    )  # kw_only для значений по умолчанию при аргументах

    _events: list[BaseEvent] = field(default_factory=list, kw_only=True)

    def register_events(self, event: BaseEvent):
        self._events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        registered_events = self._events.copy()
        self._events.clear()
        return registered_events

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "BaseEntity") -> bool:
        return self.oid == __value.oid
