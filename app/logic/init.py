from functools import lru_cache
from dishka import Provider, Scope, AsyncContainer, make_async_container

from motor.motor_asyncio import AsyncIOMotorClient

from infra.repositories.messages.base import BaseChatRepository
from infra.repositories.messages.mongo import MongoChatRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator
from settings.config import Config


@lru_cache(1)
def get_container() -> AsyncContainer:
    return _init_container()


def _init_container() -> AsyncContainer:
    def get_repo(config: Config) -> BaseChatRepository:
        client = AsyncIOMotorClient(host=config.mongodb_connection_uri, serverSelectionTimeoutMS=1000)
        return MongoChatRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    def get_mediator(chat_repository: BaseChatRepository) -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [CreateChatCommandHandler(chat_repository=chat_repository)],
        )
        return mediator

    def get_config() -> Config:
        return Config()

    provider = Provider()
    provider.provide(get_repo, scope=Scope.APP)
    provider.provide(get_mediator, scope=Scope.APP)
    provider.provide(get_config, scope=Scope.APP)

    container = make_async_container(provider)
    return container
