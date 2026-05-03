"""Update study progress service."""

from apps.core.repositories.protocol import CommandRepositoryProtocol
from apps.users.models.user import Person
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol

from .abstract import AbstractUserService


# FIXME: Fix `object` type hint
class UpdateProgressService(
    BaseAuditable,
    AbstractUserService[object, object],
):
    """Update the item study progress service."""

    def __init__(
        self,
        repository: CommandRepositoryProtocol[object, object],
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the service."""
        super().__init__(name=name, auditor=auditor)
        self._repository = repository

    def execute(self, user: Person, spec: object) -> object:
        """Update progress."""
        self.auditor.record(
            'progress_repository.call',
            obj=self._repository,
            spec=spec,
        )
        return self._repository.update(user, spec)
