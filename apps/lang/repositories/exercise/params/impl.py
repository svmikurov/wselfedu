"""Language exercise parameters fetch repository."""

from typing import override

from django.db.models import QuerySet

from apps.core.domains.exercise.protocol import ExerciseParametersProtocol
from apps.core.domains.protocol import NullProtocol
from apps.core.repositories.abstract import AbstractUserFetchRepository
from apps.lang.models import ExerciseConditions
from apps.users.models import Person


class RegularTranslationPresentationRepository(
    AbstractUserFetchRepository[NullProtocol, ExerciseParametersProtocol],
):
    """Language exercise translation parameters fetch repository."""

    @override
    def fetch(
        self,
        user: Person,
        filter: NullProtocol,
    ) -> ExerciseParametersProtocol:
        """Fetch exercise parameters DTO."""
        raise NotImplementedError

    def _fetch_conditions(
        self,
        user: Person,
        filter: NullProtocol,
    ) -> QuerySet[ExerciseConditions]:
        """Fetch exercise conditions."""
        raise NotImplementedError
