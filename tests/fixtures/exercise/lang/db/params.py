"""Language discipline exercise parameters fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.lang.models import (
    ExerciseConditions,
    PresentationSettings,
    TranslationConfiguration,
)

if TYPE_CHECKING:
    from apps.users.models import Person
    from ports.interfaces.protocols.domain.exercise import (
        ConditionsProtocol,
        ExerciseConfigProtocol,
        ExerciseSettingsProtocol,
    )


@pytest.fixture
def db_translation_lockup_conditions(
    user: Person,
    translation_lockup_conditions: ConditionsProtocol,
) -> ConditionsProtocol:
    """Provide land discipline exercise conditions."""
    ExerciseConditions.objects.create(
        user=user,
        category_id=translation_lockup_conditions.category,
        # FIXME: Fix mark field
        mark_id=translation_lockup_conditions.mark[0]
        if translation_lockup_conditions.mark
        else None,
        word_source_id=translation_lockup_conditions.source,
        start_period_id=translation_lockup_conditions.start_period,
        end_period_id=translation_lockup_conditions.end_period,
        is_study=translation_lockup_conditions.is_study,
        is_repeat=translation_lockup_conditions.is_repeat,
        is_examine=translation_lockup_conditions.is_examine,
        is_know=translation_lockup_conditions.is_know,
    )
    return translation_lockup_conditions


@pytest.fixture
def db_presentation_settings(
    user: Person,
    exercise_settings: ExerciseSettingsProtocol,
) -> ExerciseSettingsProtocol:
    """Provide presentations exercise settings."""
    PresentationSettings.objects.create(
        user=user,
        question_timeout=exercise_settings.question_timeout,
        answer_timeout=exercise_settings.answer_timeout,
    )
    return exercise_settings


@pytest.fixture
def db_exercise_configuration(
    user: Person,
    presentation_configuration: ExerciseConfigProtocol,
) -> ExerciseConfigProtocol:
    """Provide presentations exercise configuration."""
    TranslationConfiguration.objects.create(
        user=user,
        display_order=presentation_configuration.display_order,
        word_count=presentation_configuration.item_count,
    )
    return presentation_configuration
