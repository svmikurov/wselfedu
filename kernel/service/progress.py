"""Update study progress service."""

from apps.users.models.user import Person
from interfaces.schemas.service.exercise import UpdateProgressCase
from ports.abstract.service import AbstractUserSpecService
from ports.contract.enums import ExerciseStatus
from ports.contract.infra.repository import CommandRepositoryProtocol
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol


# FIXME: Fix `object` type hint
class UpdateProgressService(
    BaseAuditable,
    AbstractUserSpecService[object, object],
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
        self._repository.update(user, spec)
        return UpdateProgressCase(
            status=ExerciseStatus.UPDATED_PROGRESS,
            domain=None,
        )
