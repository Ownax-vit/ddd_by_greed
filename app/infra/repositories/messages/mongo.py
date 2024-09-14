from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient

from domain.entities.messages import Chat
from infra.repositories.messages.base import BaseChatRepository
from infra.repositories.messages.converters import convert_entity_to_document


@dataclass
class MongoChatRepository(BaseChatRepository):
    mongo_db_client: AsyncIOMotorClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    def __get_chat_collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][
            self.mongo_db_collection_name
        ]

    async def check_chat_exists_by_title(self, title: str) -> bool:
        collection = self.__get_chat_collection()
        return bool(await collection.find_one(filter={"title": title}))

    async def add_chat(self, chat: Chat) -> None:
        collection = self.__get_chat_collection()
        await collection.insert_one(convert_entity_to_document(chat=chat))
