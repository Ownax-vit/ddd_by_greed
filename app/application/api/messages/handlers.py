from fastapi import APIRouter, Depends, HTTPException, Query, status
from dishka import AsyncContainer

from infra.repositories.messages.filters import GetMessagesFilter
from logic.queries.messages import GetChatDetailQuery, GetMessagesQuery
from application.api.messages.schemas import (
    ChatDetailSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
    GetMessagesQueryResponseSchema,
    MessageDetailSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand, CreateMessageCommand
from logic.init import get_container
from logic.mediator import Mediator


router = APIRouter(tags=["Chat"])


@router.post(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(
    schema: CreateChatRequestSchema, container: AsyncContainer = Depends(get_container)
) -> CreateChatResponseSchema:
    mediator: Mediator = await container.get(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateChatResponseSchema.from_entity(chat=chat)


@router.post(
    "/{chat_oid}/messages",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageRequestSchema,
    container: AsyncContainer = Depends(get_container),
) -> CreateMessageResponseSchema:
    mediator: Mediator = await container.get(Mediator)

    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_oid=chat_oid)
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateMessageResponseSchema.from_entity(message=message)


@router.get(
    "/{chat_oid}",
    responses={
        status.HTTP_200_OK: {"model": ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def receive_chat_handler(
    chat_oid: str,
    container: AsyncContainer = Depends(get_container),
) -> ChatDetailSchema:
    mediator: Mediator = await container.get(Mediator)

    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return ChatDetailSchema.from_entity(chat=chat)


@router.get(
    "/{chat_oid}/messages/",
    responses={
        status.HTTP_200_OK: {"model": GetMessagesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def receive_messages_handler(
    chat_oid: str,
    offset: int = Query(),
    limit: int = Query(),
    container: AsyncContainer = Depends(get_container),
) -> GetMessagesQueryResponseSchema:
    mediator: Mediator = await container.get(Mediator)

    try:
        messages, count = await mediator.handle_query(
            GetMessagesQuery(
                chat_oid=chat_oid, filters=GetMessagesFilter(limit=limit, offset=offset)
            )
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return GetMessagesQueryResponseSchema(
        count=count,
        items=[MessageDetailSchema.from_entity(msg) for msg in messages],
        limit=limit,
        offset=offset,
    )
