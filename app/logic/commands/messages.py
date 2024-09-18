from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from domain.values.messages import Text, Title
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.messages import (
    ChatNotFoundException,
    ChatWithThatTitleAlreadyExistsException,
)


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chats_repository.check_chat_exists_by_title(title=command.title):
            raise ChatWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)

        # events
        new_chat = Chat.create_chat(title=title)
        await self.chats_repository.add_chat(new_chat)

        return new_chat


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass
class CreateMessageCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    messages_repository: BaseMessagesRepository
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat = await self.chats_repository.get_chat_by_oid(command.chat_oid)
        if not chat:
            raise ChatNotFoundException(command.chat_oid)

        message = Message(
            chat_oid=chat.oid, text=Text(command.text)
        )
        await self.messages_repository.add_message(message=message)
        chat.add_message(message=message)
        return message
