from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient

from domain.entities.messages import Chat, Message
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from infra.repositories.messages.converters import (
    convert_chat_document_to_entity,
    convert_entity_to_document,
    convert_message_to_document,
)


@dataclass
class BaseMongoRepository:
    mongo_db_client: AsyncIOMotorClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][
            self.mongo_db_collection_name
        ]


@dataclass
class MongoChatsRepository(BaseChatsRepository, BaseMongoRepository):
    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={"title": title}))

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter={"oid": oid})

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_entity_to_document(chat=chat))


@dataclass
class MongoMessagesRepository(BaseMessagesRepository, BaseMongoRepository):
    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(
            document=convert_message_to_document(message=message)
        )
