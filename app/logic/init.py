from functools import lru_cache
from dishka import Provider, Scope, AsyncContainer, make_async_container

from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator


@lru_cache(1)
def get_container() -> AsyncContainer:
    return _init_container()


def _init_container() -> AsyncContainer:
    def get_repo() -> BaseChatRepository:
        return MemoryChatRepository()

    def get_mediator(chat_repository: BaseChatRepository) -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [CreateChatCommandHandler(chat_repository=chat_repository)],
        )
        return mediator

    provider = Provider()
    provider.provide(get_repo, scope=Scope.APP)
    provider.provide(get_mediator, scope=Scope.APP)

    container = make_async_container(provider)
    return container
