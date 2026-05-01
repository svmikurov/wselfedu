"""Update study progress service."""

from apps.core.repositories.abstract import AbstractProgressRepository
from apps.users.models.user import Person

from .abstract import AbstractUserService


class UpdateProgressService(AbstractUserService[object, object]):
    """Update the item study progress service."""

    def __init__(
        self,
        repository: AbstractProgressRepository,
    ) -> None:
        """Construct the service."""
        self._repository = repository

    def execute(self, user: Person, spec: object) -> object:
        """Update progress."""
        pk = 1
        delta = 1
        return self._repository.update(user, pk, delta)
