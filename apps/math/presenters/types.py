"""Math app presenter types."""

from typing import NotRequired, TypedDict

from apps.core.types import RelatedDataType, ResultType

from ..services.types import CalcTaskType


class _ResponseType(TypedDict):
    """Base response type."""

    status: str
    related_data: NotRequired[RelatedDataType]


class QuestionResponseType(_ResponseType):
    """Question response type."""

    data: CalcTaskType


class ResultResponseType(_ResponseType):
    """User answer check result response type."""

    data: ResultType
