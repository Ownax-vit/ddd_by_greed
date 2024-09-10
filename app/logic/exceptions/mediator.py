from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class EventHandlerNotRegisteredException(LogicException):
    event_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для события {self.event_type}"


@dataclass(eq=False)
class CommandHandlerNotRegisteredException(LogicException):
    event_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для события {self.event_type}"
