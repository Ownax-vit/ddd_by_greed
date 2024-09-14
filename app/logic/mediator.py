from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from domain.events.base import BaseEvent
from logic.commands.base import CR, CT, CommandHandler
from logic.events.base import ER, ET, EventHandler
from logic.exceptions.mediator import (
    CommandHandlerNotRegisteredException,
    EventHandlerNotRegisteredException,
)


@dataclass(eq=False)
class Mediator:
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    commands_map: dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event].extend(event_handlers)

    def register_command(
        self, command: CT, event_handlers: Iterable[CommandHandler[CT, CR]]
    ):
        self.commands_map[command].extend(event_handlers)

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        event_type = events.__class__
        handlers = self.events_map.get(event_type)

        if not handlers:
            raise EventHandlerNotRegisteredException(event_type=event_type)

        result = []

        for event in events:
            result.extend(await handler.handle(event) for handler in handlers)

        return result

    async def handle_command(self, command: CommandHandler) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlerNotRegisteredException(command_type)

        return [await handler.handle(command) for handler in handlers]
