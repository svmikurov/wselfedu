"""Calculation web exercise validators."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.math.validators.web import exercise as validators


class ExerciseWebValidatorContainer(DeclarativeContainer):
    """Calculation web exercise validators."""

    create_regular_calculation = Factory(
        validators.RegularCalculationStartWebValidator,
    )
    check_regular_calculation = Factory(
        validators.RegularCalculationCheckWebValidator,
    )
