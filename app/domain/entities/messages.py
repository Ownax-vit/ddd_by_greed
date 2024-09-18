from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.events.messages import NewChatCreated, NewMessageReceivedEvent
from domain.values.messages import Text, Title


@dataclass(eq=False)
class Message(BaseEntity):
    _hash_ = BaseEntity.__hash__
    chat_oid: str
    text: Text


@dataclass(eq=False)
class Chat(BaseEntity):
    _hash_ = BaseEntity.__hash__

    title: Title
    messages: set[Message] = field(default_factory=set, kw_only=True)

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_events(
            NewMessageReceivedEvent(
                message_text=message.text.as_generic_type(),
                chat_oid=self.oid,
                message_oid=message.oid,
            )
        )

    @classmethod
    def create_chat(cls, title: Title) -> "Chat":
        new_chat = cls(title=title)
        new_chat.register_events(
            NewChatCreated(
                chat_oid=new_chat.oid,
                chat_title=new_chat.title,
            )
        )

        return new_chat
