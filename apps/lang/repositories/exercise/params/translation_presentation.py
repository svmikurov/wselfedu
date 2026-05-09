"""Language exercise parameters fetch repository."""

from typing import Any, override

from django.db.models import Manager, Model

from apps.core.domains.exercise.protocol import ExerciseParametersProtocol
from apps.core.repositories.abstract import AbstractUserFetchRepository
from apps.lang.models import (
    ExerciseConditions,
    PresentationSettings,
    TranslationConfiguration,
)
from apps.users.models import Person
from contracts import NullProtocol
from contracts.enums.exercise import DisplayOrder
from contracts.schemas.domain.exercise.params import (
    ExerciseConfigDTO,
    ExerciseParametersDTO,
    ExerciseSettingsDTO,
    LookupConditionsDTO,
)


# REVIEW: Exercise parameters repo
class RegularTranslationPresentationRepository(
    AbstractUserFetchRepository[NullProtocol, ExerciseParametersProtocol],
):
    """Language translation presentation parameters fetch repository."""

    def __init__(
        self,
        conditions_manager: Manager[ExerciseConditions],
        config_manager: Manager[PresentationSettings],
        settings_manager: Manager[TranslationConfiguration],
    ) -> None:
        """Construct the repository."""
        self._conditions = conditions_manager
        self._config = config_manager
        self._settings = settings_manager

    @override
    def fetch(
        self,
        user: Person,
        filter: NullProtocol,
    ) -> ExerciseParametersProtocol:
        """Fetch exercise parameters DTO."""
        return ExerciseParametersDTO(
            conditions=self._fetch_conditions(user, filter),
            settings=self._fetch_settings(user, filter),
            conf=self._fetch_configuration(user, filter),
        )

    def _fetch_conditions(
        self,
        user: Person,
        filter: NullProtocol,
    ) -> LookupConditionsDTO:
        """Fetch exercise conditions."""
        params = self._conditions.filter(user=user).first()
        if params is None:
            return LookupConditionsDTO()

        progress: dict[str, bool] = {}
        for attr in ('is_study', 'is_repeat', 'is_examine', 'is_know'):
            progress[attr] = getattr(params, attr)

        return LookupConditionsDTO(
            category=self._get_pk(params.category),
            source=self._get_pk(params.word_source),
            mark=[params.mark.pk] if params.mark else [],
            start_period=self._get_pk(params.start_period),
            end_period=self._get_pk(params.end_period),
            **progress,
        )

    def _fetch_settings(
        self,
        user: Person,
        filter: NullProtocol,
    ) -> ExerciseSettingsDTO:
        """Fetch exercise settings."""
        settings = self._config.filter(user=user).first()
        if settings is None:
            return ExerciseSettingsDTO()

        return ExerciseSettingsDTO(
            question_timeout=settings.question_timeout,
            answer_timeout=settings.answer_timeout,
        )

    def _fetch_configuration(
        self,
        user: Person,
        filter: NullProtocol,
    ) -> ExerciseConfigDTO:
        """Fetch exercise configuration."""
        conf = self._settings.filter(user=user).first()
        if conf is None:
            return ExerciseConfigDTO()

        data: dict[str, Any] = {}
        if display_order := conf.display_order:
            data['display_order'] = DisplayOrder(display_order)
        if item_count := conf.word_count:
            data['item_count'] = item_count

        return ExerciseConfigDTO(**data)

    @staticmethod
    def _get_pk(instance: Model | None) -> int | None:
        return int(instance.pk) if instance else None
