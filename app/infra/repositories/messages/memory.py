from dataclasses import dataclass, field
from collections import defaultdict
from typing import Iterable

from infra.repositories.messages.filters import GetMessagesFilter
from domain.entities.messages import Chat, Message
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository


@dataclass
class MemoryChatsRepository(BaseChatsRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        try:
            return bool(next(chat for chat in self._saved_chats if chat.oid == oid))
        except StopIteration:
            return None

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(
                    chat
                    for chat in self._saved_chats
                    if chat.title.as_generic_type() == title
                )
            )
        except StopIteration:
            return False

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)


class MemoryMessagesRepository(BaseMessagesRepository):
    _saved_messages: dict[str, list[Message]] = field(
        default_factory=defaultdict(list), kw_only=True
    )

    async def add_message(self, message: Message) -> None:
        self[message.chat_oid].append(message)

    async def get_messages(
        self, chat_oid: str, filters: GetMessagesFilter
    ) -> tuple[Iterable[Message], int]:
        messages = self._saved_messages[chat_oid]

        return messages[filters.offset:filters.offset + filters.limit]
