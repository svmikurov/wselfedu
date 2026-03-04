"""Test calculation performing by student."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from apps.math.models import (
    CalculationCondition,
    CalculationTypeChoices,
    StudentCalculationCondition,
)
from apps.study.models import (
    ExerciseAvailability,
    ExerciseReward,
    PeriodExecuting,
    RewardType,
)
from apps.users.models import Mentorship
from tests.browser.pages.math.student.calculation_perform import (
    StudentCalculationPerformPage,
)
from tests.browser.tests import base, mixins

if TYPE_CHECKING:
    from apps.users.models import Person


@pytest.fixture
def calculation_condition(
    mentor: Person,
) -> CalculationCondition:
    """Populate DB with mentor`s calculation exercise conditions."""
    return CalculationCondition.objects.create(
        name='adding',
        min_operand=2,
        max_operand=3,
        operation_type=CalculationTypeChoices.ADD,
        user=mentor,
    )


@pytest.fixture
def calculation_assignation(
    calculation_condition: CalculationCondition,
    mentorship: Mentorship,
) -> StudentCalculationCondition:
    """Populate DB with assigned calculation exercise for student."""
    # Exercise assignation
    assignation = StudentCalculationCondition.objects.create(
        calculation_condition=calculation_condition,
        mentorship=mentorship,
    )
    # Exercise availability
    ExerciseAvailability.objects.create(
        exercise_content_type=ContentType.objects.get_for_model(assignation),
        exercise_object_id=assignation.pk,
        required_count=10,
        period_type=PeriodExecuting.DAILY,
    )
    # Exercise reward
    ExerciseReward.objects.create(
        exercise_content_type=ContentType.objects.get_for_model(assignation),
        exercise_object_id=assignation.pk,
        reward_type=RewardType.PER_CASE,
        amount=1,
    )
    return assignation


class StudentCalculationPerformTest(
    mixins.OpenPageMixin[StudentCalculationPerformPage],
    base.BaseAuthTest,
):
    """Test calculation performing by student.

    Test via mixin that:
        - response status code is OK
        - page have correct title
    """

    @pytest.fixture(autouse=True)
    def set_user(self, student: Person) -> None:
        """Set user."""
        self.user = student

    @pytest.fixture(autouse=True)
    def set_path(self, calculation_assignation: CalculationCondition) -> None:
        """Set up page path."""
        self._path = str(
            reverse(
                'math:student_calculation_exercise',
                kwargs={'pk': calculation_assignation.pk},
            )
        )

    def setUp(self) -> None:
        """Set up page."""
        super().setUp()

        self.page = StudentCalculationPerformPage(self._page, self._path)
        self.page.open()
