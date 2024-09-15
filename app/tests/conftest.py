from dishka import AsyncContainer
from pytest import fixture
import pytest_asyncio

from infra.repositories.messages.base import BaseChatsRepository
from logic.mediator import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> AsyncContainer:
    return init_dummy_container()


@pytest_asyncio.fixture(name="chat_repository")
async def repo(container: AsyncContainer) -> BaseChatsRepository:
    repo: BaseChatsRepository = await container.get(BaseChatsRepository)
    return repo


@pytest_asyncio.fixture
async def mediator(container: AsyncContainer) -> Mediator:
    mediator: Mediator = await container.get(Mediator)
    return mediator
