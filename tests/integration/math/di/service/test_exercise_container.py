"""Exercise container dependency tests."""

from apps.math.di.service.exercise import ExerciseServiceContainer

CONTAINER = ExerciseServiceContainer


class CreateCalculationCaseInitializeTest:
    """Create calculation case initialize test."""

    def test_create_calculation_case(self) -> None:
        """Create calculation case initialized success."""
        assert CONTAINER.create_calculation_case
