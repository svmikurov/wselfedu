"""General DTO fields."""

from typing import Generic, TypeVar

from pydantic import Field

from interfaces.schemas.base import BaseDTO

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
