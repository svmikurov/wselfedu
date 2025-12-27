"""Get presentation service."""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING

from ..schemas import dto

if TYPE_CHECKING:
    from apps.core.storage import services as storage
    from apps.users.models import Person

    from .. import domain, repositories, schemas

    # Dependencies
    type Repository = repositories.EnglishTranslation
    type Domain = domain.PresentationDomain
    type Storage = storage.TaskStorage[CaseMeta]

    # Data
    type PresentationRequest = schemas.PresentationRequest
    type Case = dto.PresentationCase
    type CaseMeta = dto.CaseMeta


class PresentationService:
    """Get presentation service."""

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

    def execute(self, user: Person, request: PresentationRequest) -> Case:
        """Build and return presentation case."""
        candidates = self._repository.fetch(user, request.parameters)
        case, case_meta = self._domain.get_case(candidates, request.settings)
        case_uuid = self._storage.save_task(case_meta)
        return dto.PresentationCase(**asdict(case), case_uuid=case_uuid)
