"""Exercise completion service tests."""

from __future__ import annotations

import pytest
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from apps.math.domains.dto import (
    ExerciseAvailabilityDTO,
    ExerciseCompletionDTO,
)
from apps.math.models import StudentCalculationCondition
from apps.study.models import ExerciseLog, PeriodExecuting
from apps.study.services.completion import ExerciseCompletionService


@pytest.fixture
def service() -> ExerciseCompletionService[StudentCalculationCondition]:
    """Provide exercise completion service."""
    return ExerciseCompletionService(StudentCalculationCondition.objects)


@pytest.fixture
def content_type() -> ContentType:
    """Provide content type for StudentCalculationCondition."""
    return ContentType.objects.get_for_model(StudentCalculationCondition)


@pytest.mark.django_db
class TestStudentCalculationCompletionService:
    """Student's calculation completion assigned exercise test."""

    @pytest.mark.parametrize(
        'required_count, initial_success_count, expected_success_count',
        (
            (10, 0, 1),
            (10, 4, 5),
            (10, 10, 10),
        ),
    )
    def test_correct_answer(
        self,
        required_count: int,
        initial_success_count: int,
        expected_success_count: int,
        service: ExerciseCompletionService[StudentCalculationCondition],
        calculation_assignation: StudentCalculationCondition,
        content_type: ContentType,
    ) -> None:
        """Test the calculation with correct answer."""
        # Arrange
        availability = ExerciseAvailabilityDTO(
            required_count=required_count,
            period_type=PeriodExecuting.DAILY,
        )
        # The current value of successfully completed
        # tasks is cached when the task is created.
        completion = ExerciseCompletionDTO(
            success_count=initial_success_count,
            failure_count=0,
            tracking_date=timezone.now(),
        )
        ExerciseLog.objects.create(
            exercise_content_type=content_type,
            exercise_object_id=calculation_assignation.pk,
            success_count=initial_success_count,
            failure_count=0,
        )

        # Act
        service.add_success(
            calculation_assignation.pk,
            availability,
            completion,
        )

        # Assert
        log = ExerciseLog.objects.get(
            exercise_content_type=content_type,
            exercise_object_id=calculation_assignation.pk,
        )
        assert log.success_count == expected_success_count
