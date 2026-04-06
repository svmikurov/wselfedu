"""Abstract base class for repository."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from django.db.models import Model

from apps.users.models import Person

from .protocol import ModelRepositoryProtocol, UserRepositoryProtocol

FilterT = TypeVar('FilterT')
ModelT = TypeVar('ModelT', bound=Model)
ResultT = TypeVar('ResultT')


class AbstractModelRepository(
    ABC,
    ModelRepositoryProtocol[FilterT, ModelT],
):
    """ABC for model repository."""

    @override
    @abstractmethod
    def get_query(self, filter: FilterT) -> ModelT:
        """Fetch model."""


class AbstractUserFetchRepository(
    ABC,
    UserRepositoryProtocol[FilterT, ResultT],
):
    """ABC for fetch repository via user filter."""

    @override
    @abstractmethod
    def fetch(self, user: Person, filter: FilterT) -> ResultT:
        """Fetch."""
