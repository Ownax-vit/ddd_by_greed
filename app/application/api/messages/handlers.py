from fastapi import APIRouter, Depends, HTTPException, status
from dishka import AsyncContainer

from application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand
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
        chat, *_ = await mediator.handle_command(
            CreateChatCommand(title=schema.title)
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateChatResponseSchema.from_entity(chat=chat)
