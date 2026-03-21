"""Language exercise parameters fetch repository."""

from typing import TypedDict, TypeVar, override

from django.db.models import Manager, Model

from apps.core.domains.abstract import AbstractDTOFactory
from apps.core.domains.protocol import DTOFactoryProtocol
from apps.core.repositories.abstract import AbstractRepository
from apps.core.repositories.protocol import ModelRepositoryProtocol
from apps.users.models import Person

from .dto import ExerciseParametersDTO

ModelT = TypeVar('ModelT', bound=Model)
ModelManager = TypeVar('ModelManager', bound=Manager[Model])


class _QueryFilter(TypedDict):
    """Database query filter."""

    user: Person


class ExerciseParametersDTOFactory(
    AbstractDTOFactory[ModelT, ExerciseParametersDTO]
):
    """Exercise parameters DTO factory."""

    @override
    def build(self, data: ModelT) -> ExerciseParametersDTO:
        """Build exercise parameters DTO."""
        return ExerciseParametersDTO()


class ExerciseParametersRepository(
    AbstractRepository[_QueryFilter, ExerciseParametersDTO],
    ModelRepositoryProtocol[_QueryFilter, ModelT],
):
    """Language exercise parameters fetch repository."""

    def __init__(
        self,
        manager: Manager[ModelT],
        dto_factory: DTOFactoryProtocol[ModelT, ExerciseParametersDTO],
    ) -> None:
        """Construct the repository."""
        self._manager = manager
        self._dto_factory = dto_factory

    @override
    def fetch(self, filter: _QueryFilter) -> ExerciseParametersDTO:
        """Fetch exercise parameters DTO."""
        return self._dto_factory.build(self.get_query(filter))

    @override
    def get_query(self, filter: _QueryFilter) -> ModelT:
        """Get exercise parameters query."""
        return self._manager.get(**filter)
