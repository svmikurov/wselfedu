"""Abstract base class for repository."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from django.db.models import Model

from .protocol import ModelRepositoryProtocol, RepositoryProtocol

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
    RepositoryProtocol[FilterData, ResultT],
):
    """ABC for DTO repository."""

    @override
    @abstractmethod
    def fetch(self, filter: FilterData) -> ResultT:
        """Fetch data."""
