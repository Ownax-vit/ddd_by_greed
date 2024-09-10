import pytest

from domain.entities.messages import Chat
from infra.repositories.messages import BaseChatRepository
from logic.commands.messages import CreateChatCommand
from logic.mediator import Mediator


@pytest.mark.asyncio
def test_create_chat_command_success(
    chat_repo: BaseChatRepository,
    mediator: Mediator,
):
    chat: Chat = mediator.handle_command(
        CreateChatCommand(title="megaTitle", chat_repo=chat_repo),
    )

    assert chat_repo.check_chat_exists_by_title(title=chat.title.as_generic_type())
