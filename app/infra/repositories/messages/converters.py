from typing import Any, Mapping
from domain.values.messages import Text, Title
from domain.entities.messages import Chat, Message


def convert_message_to_document(message: Message) -> dict:
    return {"oid": message.oid, "text": message.text.as_generic_type()}


def convert_entity_to_document(chat: Chat) -> dict:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "messages": [convert_message_to_document(message) for message in chat.messages],
        "created_at": chat.created_at,
    }


def convert_message_to_entity(message: Mapping[str, Any]) -> Message:
    return Message(
        text=Text(message["text"]),
        oid=message["oid"],
        created_at=message["created_at"],
    )


def convert_chat_document_to_entity(chat: Mapping[str, Any]) -> Chat:
    return Chat(
        title=Title(chat["title"]),
        oid=chat["oid"],
        created_at=chat["created_at"],
        messages={convert_message_to_entity(message) for message in chat["messages"]},
    )
