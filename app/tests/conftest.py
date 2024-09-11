from dishka import AsyncContainer
from pytest import fixture
import pytest_asyncio

from infra.repositories.messages import BaseChatRepository
from logic.mediator import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope="session")
def container() -> AsyncContainer:
    return init_dummy_container()


@pytest_asyncio.fixture(scope="package", name="chat_repository")
async def repo(container: AsyncContainer) -> BaseChatRepository:
    repo: BaseChatRepository = await container.get(BaseChatRepository)
    return repo


@pytest_asyncio.fixture(scope="package")
async def mediator(container: AsyncContainer) -> Mediator:
    mediator: Mediator = await container.get(Mediator)
    return mediator
