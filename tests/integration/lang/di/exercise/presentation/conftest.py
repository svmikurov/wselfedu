"""Language discipline presentation exercise DI tests."""

import pytest

from di import MainContainer

from ._types import HandlerT


@pytest.fixture
def regular_presentation_handler(
    main_container: MainContainer,
) -> HandlerT:
    """Provide regular presentation exercise handler fixture."""
    return main_container.lang.handlers.regular_translation_presentation  # type: ignore
