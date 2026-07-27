"""Application layer protocols."""

from typing import Protocol, TypeVar

from wse.domain.events import Event

Command_contra = TypeVar('Command_contra', contravariant=True)
HandlerResultT = TypeVar('HandlerResultT')
Result_co = TypeVar('Result_co', covariant=True)


class Executable(Protocol[Command_contra, Result_co]):
    def execute(self, cmd: Command_contra) -> Result_co: ...


class EventResultCollectable(Protocol[HandlerResultT, Result_co]):
    def collect(
        self,
        events: list[Event],
        handler_results: list[HandlerResultT],
    ) -> Result_co: ...
