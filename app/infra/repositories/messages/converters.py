from typing import Any, Mapping
from domain.values.messages import Text, Title
from domain.entities.messages import Chat, Message


def convert_message_to_document(message: Message) -> dict:
    return {
        "oid": message.oid,
        "chat_oid": message.chat_oid,
        "text": message.text.as_generic_type(),
        "created_at": message.created_at,
    }


def convert_entity_to_document(chat: Chat) -> dict:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "created_at": chat.created_at,
    }


def convert_message_to_entity(message: Mapping[str, Any]) -> Message:
    return Message(
        text=Text(message["text"]).as_generic_type(),
        oid=message["oid"],
        created_at=message["created_at"],
        chat_oid=message["chat_oid"],
    )


def convert_chat_document_to_entity(chat: Mapping[str, Any]) -> Chat:
    return Chat(
        title=Title(chat["title"]),
        oid=chat["oid"],
        created_at=chat["created_at"],
    )
