"""Get presentation service."""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.core.domains.exercise.schema.presentation_dto import (
    PresentationData,
    PresentationMeta,
)
from apps.lang.schemas import dto

if TYPE_CHECKING:
    from apps.core.domains.exercise.presentation import (
        PresentationDomain,
    )
    from apps.core.storages import services as storage
    from apps.lang import repositories
    from apps.lang.use_cases.exercise.types import (
        RegularRequest,
    )
    from apps.users.models import Person

    type Repository = repositories.TranslationConditionsRepository
    type Domain = PresentationDomain
    type Storage = storage.TaskStorage[PresentationMeta]

    type CaseMeta = dto.CaseMeta


class PresentationService:
    """Get presentation exercise service."""

    def __init__(
        self,
        repository: Repository,
        domain: Domain,
        storage: Storage,
    ) -> None:
        """Construct the service."""
        self._repository = repository
        self._domain = domain
        self._storage = storage

    def execute(
        self, user: Person, request: RegularRequest
    ) -> PresentationData:
        """Build and return exercise case."""
        candidates = self._repository.fetch(user, request.parameters)

        case, case_meta = self._domain.execute(candidates, request.settings)  # type: ignore
        case_uuid = self._storage.save_task(case_meta)
        return PresentationData(
            case_uuid=case_uuid,
            question_text=case.question_text,
            answer_text=case.answer_text,
            progress=case.progress,
        )
