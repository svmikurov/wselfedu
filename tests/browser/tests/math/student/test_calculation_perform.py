"""Test calculation performing by student."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from apps.math.models import CalculationCondition
from tests.browser.pages.math.student.calculation_perform import (
    StudentCalculationPerformPage,
)
from tests.browser.tests import base, mixins

if TYPE_CHECKING:
    from apps.users.models import Person


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
