"""General DTO fields."""

from typing import Generic, TypeVar

from pydantic import Field

from ports.interfaces.schemas.base import ArbitraryDTO, BaseDTO

T = TypeVar('T')

StatusT = TypeVar('StatusT')


class ResourceIdentifierField(BaseDTO):
    """Database resource identifier DTO field."""

    pk: int = Field(
        description='Database item ID',
    )


class StatusField(BaseDTO, Generic[StatusT]):
    """Exercise status DTO's field."""

    status: StatusT = Field(
        description='Status',
    )


class TextField(BaseDTO):
    """Text value DTO field."""

    text: str = Field(
        description='Display option text',
    )


class ValueField(BaseDTO):
    """Value DTO's field."""

    value: int = Field(
        description='Value',
    )


class ExceptionField(ArbitraryDTO, Generic[T]):
    """Provides *exception* DTO's field."""

    exception: T


class TaskField(BaseDTO, Generic[T]):
    """Provides *task* DTO's field."""

    task: T


class DomainField(BaseDTO, Generic[T]):
    """Provides *domain* DTO generic field."""

    domain: T | None


class OptionDomainField(BaseDTO, Generic[T]):
    """Provides option *domain* DTO generic field."""

    domain: T
