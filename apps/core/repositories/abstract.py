"""Abstract base class for repository."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from django.db.models import Model

from apps.users.models import Person

from .protocol import ModelRepositoryProtocol, UserRepositoryProtocol

FilterData = TypeVar('FilterData')
ModelT = TypeVar('ModelT', bound=Model)
ResultT = TypeVar('ResultT')


class AbstractModelRepository(
    ABC,
    ModelRepositoryProtocol[FilterData, ModelT],
):
    """ABC for model repository."""

    @override
    @abstractmethod
    def get_query(self, filter: FilterData) -> ModelT:
        """Fetch model."""


class AbstractRepository(
    ABC,
    UserRepositoryProtocol[FilterData, ResultT],
):
    """ABC for DTO repository."""

    @override
    @abstractmethod
    def fetch(self, user: Person, filter: FilterData) -> ResultT:
        """Fetch data."""
