from functools import lru_cache
from dishka import AsyncContainer, Provider, make_async_container, Scope
from pytest import Config

from infra.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from infra.repositories.messages.memory import (
    MemoryChatsRepository,
    MemoryMessagesRepository,
)
from logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from logic.mediator import Mediator
from logic.queries.messages import GetChatDetailQuery, GetChatDetailQueryHandler


@lru_cache(1)
def init_dummy_container() -> AsyncContainer:
    return _init_container()


def _init_container() -> AsyncContainer:
    def get_repo_chats() -> BaseChatsRepository:
        return MemoryChatsRepository()

    def get_repo_messages() -> BaseMessagesRepository:
        return MemoryMessagesRepository()

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
    provider.provide(get_repo_chats, scope=Scope.APP)
    provider.provide(get_repo_messages, scope=Scope.APP)
    provider.provide(get_mediator, scope=Scope.APP)
    provider.provide(get_config, scope=Scope.APP)

    container = make_async_container(provider)
    return container
