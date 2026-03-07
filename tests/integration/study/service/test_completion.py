"""Exercise completion service tests."""

from __future__ import annotations

from typing import Protocol

import pytest
from django.contrib.contenttypes.models import ContentType

from apps.math.models import (
    StudentCalculationCondition,
)
from apps.study.models import ExerciseLog
from apps.study.services.completion import ExerciseCompletionService


class ExerciseLogCreator(Protocol):
    """Protocol for exercise log."""

    def __call__(
        self, success_count: int = 0, failure_count: int = 0
    ) -> ExerciseLog:
        """Call."""


@pytest.fixture
def service() -> ExerciseCompletionService[StudentCalculationCondition]:
    """Provide exercise completion service."""
    return ExerciseCompletionService(StudentCalculationCondition.objects)


@pytest.fixture
def content_type() -> ContentType:
    """Provide content type for StudentCalculationCondition."""
    return ContentType.objects.get_for_model(StudentCalculationCondition)


@pytest.fixture
def exercise_log(
    calculation_assignation: StudentCalculationCondition,
    content_type: ContentType,
) -> ExerciseLogCreator:
    """Provide exercise log with custom success_count."""

    def _get_log(
        success_count: int = 0,
        failure_count: int = 0,
    ) -> ExerciseLog:
        return ExerciseLog.objects.create(
            exercise_content_type=content_type,
            exercise_object_id=calculation_assignation.pk,
            success_count=success_count,
            failure_count=failure_count,
        )

    return _get_log


@pytest.mark.django_db
class TestStudentCalculationCompletionService:
    """Student's calculation completion assigned exercise test."""

    INITIAL_COUNT = 0
    SINGLE_INCREMENT = 1

    @pytest.mark.parametrize(
        'initial_success_count,expected_success_count',
        (
            (0, 1),
            (4, 5),
        ),
    )
    def test_start_exercise_success(
        self,
        initial_success_count: int,
        expected_success_count: int,
        service: ExerciseCompletionService[StudentCalculationCondition],
        calculation_assignation: StudentCalculationCondition,
        content_type: ContentType,
        exercise_log: ExerciseLogCreator,
    ) -> None:
        """Test the start calculation with correct answer."""
        # Arrange
        exercise_log(success_count=initial_success_count)

        # Act
        service.add_success(calculation_assignation.pk)

        # Assert
        log = ExerciseLog.objects.get(
            exercise_content_type=content_type,
            exercise_object_id=calculation_assignation.pk,
        )
        assert log.success_count == expected_success_count
