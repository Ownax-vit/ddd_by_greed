from functools import lru_cache
from dishka import Provider, Scope, AsyncContainer, make_async_container

from motor.motor_asyncio import AsyncIOMotorClient

from logic.queries.messages import GetChatDetailQuery, GetChatDetailQueryHandler
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from infra.repositories.messages.mongo import (
    MongoChatsRepository,
    MongoMessagesRepository,
)
from logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from logic.mediator import Mediator
from settings.config import Config


@lru_cache(1)
def get_container() -> AsyncContainer:
    return _init_container()


def _init_container() -> AsyncContainer:
    def get_mongo_client(config: Config) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(
            host=config.mongodb_connection_uri, serverSelectionTimeoutMS=1000
        )

    def get_repo_chats(
        mongo_client: AsyncIOMotorClient, config: Config
    ) -> BaseChatsRepository:
        return MongoChatsRepository(
            mongo_db_client=mongo_client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    def get_repo_messages(
        mongo_client: AsyncIOMotorClient, config: Config
    ) -> BaseMessagesRepository:
        return MongoMessagesRepository(
            mongo_db_client=mongo_client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_messages_collection,
        )

    def get_mediator(
        chat_repository: BaseChatsRepository, message_repository: BaseMessagesRepository
    ) -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [CreateChatCommandHandler(chats_repository=chat_repository)],
        )
        mediator.register_command(
            CreateMessageCommand,
            [
                CreateMessageCommandHandler(
                    chats_repository=chat_repository,
                    messages_repository=message_repository,
                )
            ],
        )
        mediator.register_query(
            GetChatDetailQuery,
            GetChatDetailQueryHandler(
                chats_repository=chat_repository,
                messages_repository=message_repository,
            ),
        )
        return mediator

    def get_config() -> Config:
        return Config()

    provider = Provider()
    provider.provide(get_mongo_client, scope=Scope.APP)
    provider.provide(get_repo_chats, scope=Scope.APP)
    provider.provide(get_repo_messages, scope=Scope.APP)
    provider.provide(get_mediator, scope=Scope.APP)
    provider.provide(get_config, scope=Scope.APP)

    container = make_async_container(provider)
    return container
