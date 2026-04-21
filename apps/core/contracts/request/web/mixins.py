"""WEB request DTO field mixins."""

from typing import Generic, TypeAlias, TypeVar

from pydantic import BaseModel, Field

from apps.core.domains.exercise.enums import ExerciseProcessEnum

DataT: TypeAlias = dict[str, str]

PayloadT = TypeVar('PayloadT')


class PayloadField(BaseModel, Generic[PayloadT]):
    """Provides payload DTO's field."""

    payload: PayloadT = Field(
        description='Request payload',
    )


class DataField(BaseModel):
    """Provides data DTO's field."""

    payload: DataT = Field(
        description='Request data',
    )


class ExerciseProcessField(BaseModel):
    """Provides exercise process action DTO's field."""

    action: ExerciseProcessEnum = Field(
        description='Process exercise action',
    )
