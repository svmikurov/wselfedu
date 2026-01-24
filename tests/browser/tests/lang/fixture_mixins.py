"""Set up fixture mixins for page test class."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from apps.lang.models import EnglishAssignedExercise


class SetUpAssignmentFixtureMixin:
    """Provides exercise assignment fixture set up with DB populate."""

    @pytest.fixture(autouse=True)
    def set_up_assignment(self, assignment: EnglishAssignedExercise) -> None:
        """Populate DB with exercise assignation for student."""
        self.assignment = assignment
