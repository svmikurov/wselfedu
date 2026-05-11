"""Language exercise parameters fixtures."""

import pytest

from interfaces.protocols.domain.exercise import (
    ConditionsProtocol,
    ExerciseConfigProtocol,
    ExerciseSettingsProtocol,
)
from ports.interfaces.schemas.domain.exercise.params import (
    ExerciseConfigDTO,
    ExerciseSettingsDTO,
    LookupConditionsDTO,
)
from tests.fixtures.exercise.lang.no_db.translations import (
    TRANSLATION_INDEX,
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
        question_timeout=TRANSLATION_INDEX,
        answer_timeout=5,
    )
