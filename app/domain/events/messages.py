from dataclasses import dataclass
from uuid import UUID

from domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_text: str
    message_oid: str
    chat_oid: UUID


@dataclass
class NewChatCreated(BaseEvent):
    chat_oid: UUID
    chat_title: str