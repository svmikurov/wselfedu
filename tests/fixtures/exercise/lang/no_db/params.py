"""Language exercise parameters fixtures."""

import pytest

from apps.core.domains.exercise.protocol import (
    ConditionsProtocol,
    ExerciseConfigProtocol,
    ExerciseSettingsProtocol,
)
from contracts.schemas.domain.exercise.params import (
    ExerciseConfigDTO,
    ExerciseSettingsDTO,
    LookupConditionsDTO,
)


@pytest.fixture
def translation_lockup_conditions() -> ConditionsProtocol:
    """Provide translation lockup conditions fixture."""
    return LookupConditionsDTO(
        is_know=False,
    )


@pytest.fixture
def presentation_configuration() -> ExerciseConfigProtocol:
    """Provide presentation exercise configuration fixture."""
    return ExerciseConfigDTO(
        item_count=100,
    )


@pytest.fixture
def exercise_settings() -> ExerciseSettingsProtocol:
    """Provide exercise settings fixture."""
    return ExerciseSettingsDTO(
        question_timeout=3,
        answer_timeout=5,
    )
