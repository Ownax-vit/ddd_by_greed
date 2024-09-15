from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(ApplicationException):
    title: str

    @property
    def message(self):
        return f"Чат с названием {self.title} уже существует"


@dataclass(eq=False)
class ChatNotFoundException:
    chat_oid: str

    @property
    def message(self):
        return f"Чат с {self.chat_oid=} не существует"
