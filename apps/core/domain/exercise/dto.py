"""Core domain exercise DTOs."""

from uuid import UUID

from pydantic import Field

from ..base_dto import BaseDTO


class UuidDTO(BaseDTO):
    """Stored exercise case UUID DTO."""

    case_uuid: UUID = Field(
        description='Stored exercise case UUID',
    )


class StoredCase(UuidDTO):
    """Stored exercise case."""

    case: BaseDTO


class ProgressConfigSchema(BaseDTO):
    """Iem study progress config schema."""

    increment: int
    decrement: int
