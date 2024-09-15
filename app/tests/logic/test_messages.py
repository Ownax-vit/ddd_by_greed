import pytest

from faker import Faker

from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.messages.base import BaseChatsRepository
from logic.commands.messages import CreateChatCommand
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chat_repository: BaseChatsRepository, mediator: Mediator, faker: Faker
):
    title = Title(faker.text())
    chat: Chat
    chat, *_ = await mediator.handle_command(
        CreateChatCommand(title=title.as_generic_type()),
    )

    assert await chat_repository.check_chat_exists_by_title(
        title=chat.title.as_generic_type()
    )


@pytest.mark.asyncio
async def test_chat_command_title_exists(
    chat_repository: BaseChatsRepository, mediator: Mediator, faker: Faker
):
    title_text = faker.text()
    chat = Chat(title=Title(title_text))

    await chat_repository.add_chat(chat=chat)

    with pytest.raises(ChatWithThatTitleAlreadyExistsException):
        chat, *_ = await mediator.handle_command(
            CreateChatCommand(title=title_text),
        )
