"""Api get presentation validator."""

from typing import Any

from apps.study.api.v1 import serializers as study

from ...core.handlers.protocol import ValidatorProtocol
from .. import schemas, types
from ..api.v1.serializers import base as lang

type RequestData = dict[str, Any]
type RequestDTO = schemas.ExerciseParametersDTO

# TODO: Update serializers to pydantic models?


class PresentationSerializer(
    lang.TranslationMetaSerializer,
    lang.TranslationSettingsSerializer,
    study.ProgressPhaseSerializer,
):
    """Get presentation serializer."""


class ApiPresentationValidator(ValidatorProtocol[RequestDTO]):
    """Api get presentation validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> RequestDTO:
        """Validate the api request presentation data."""
        serializer = PresentationSerializer(data=raw_data)
        serializer.is_valid(raise_exception=True)
        return cls._to_dto(serializer.validated_data)

    @classmethod
    def _to_dto(cls, data: types.ApiRequest) -> RequestDTO:
        """Create presentation request DTO."""
        parameters = schemas.LookupConditionsDTO(
            category=cls._get_id(data['category']),
            source=cls._get_id(data['word_source']),
            mark=cls._get_ids(data['mark']),
            start_period=cls._get_id(data['start_period']),
            end_period=cls._get_id(data['end_period']),
            is_study=data['is_study'],
            is_repeat=data['is_repeat'],
            is_examine=data['is_examine'],
            is_know=data['is_know'],
        )
        settings = schemas.ExerciseConfigDTO(
            # FIXME: Fix type ignore
            display_order=data['display_order']['code'],  # type: ignore
            item_count=data['word_count'],
        )
        return schemas.ExerciseParametersDTO(
            parameters=parameters,
            conf=settings,
        )

    @staticmethod
    def _get_id(data: types.IdName | None) -> int | None:
        """Get parameters ID or return None."""
        return data['id'] if data else None

    @staticmethod
    def _get_ids(items: list[types.IdName]) -> list[int]:
        """Get parameters IDs."""
        return [item['id'] for item in items if items]
