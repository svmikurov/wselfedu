"""Reqeust handler test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.fixtures.exercise.lang.no_db.translations import TRANSLATIONS

if TYPE_CHECKING:
    from di import MainContainer
    from ports.contract.types.handler import PresentationHandlerT
    from ports.interfaces.schemas.domain.exercise.exercise import (
        TaskItem,
    )


@pytest.fixture
def presentation_handler(
    main_container: MainContainer,
) -> PresentationHandlerT:
    """Provide presentation exercise request DI handler."""
    return main_container.lang.handlers.regular_translation_presentation()  # type: ignore


@pytest.fixture
def test_handler(
    main_container: MainContainer,
) -> PresentationHandlerT:
    """Provide test exercise request DI handler."""
    return main_container.lang.handlers.regular_translation_test()  # type: ignore


@pytest.fixture
def translation_items() -> list[TaskItem]:
    """Provide translation task items."""
    return [
        TaskItem(
            pk=pk,
            define=define,
            mean=mean,
            progress_value=0,
        )
        for pk, (define, mean) in enumerate(TRANSLATIONS, start=1)
    ]
