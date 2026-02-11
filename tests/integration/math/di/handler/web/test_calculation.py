"""Calculation handler tests."""

from di import MainContainer

CONTAINER = MainContainer.math.web_handlers


class WebCalculationConditionsTest:
    """Calculation conditions web request handler test."""

    def test_handler_initialized(self) -> None:
        """Test that handler success initialized."""
        assert CONTAINER.calculation_conditions_setup  # type: ignore[attr-defined]
