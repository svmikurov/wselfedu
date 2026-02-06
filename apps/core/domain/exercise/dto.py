"""Core domain exercise DTOs."""

from uuid import UUID

from pydantic import Field

from ..base_dto import BaseDTO


class StoredCase(BaseDTO):
    """Stored exercise case."""

    case_uuid: UUID = Field(
        description='Stored exercise case UUID',
    )
    case: BaseDTO


class ProgressConfigSchema(BaseDTO):
    """Iem study progress config schema."""

    increment: int
    decrement: int


class UUIDMixin(BaseDTO):
    """Provides UUID pydantic field."""

    case_uuid: UUID = Field(
        description='Stored exercise case UUID',
    )
