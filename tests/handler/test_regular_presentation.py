"""Language discipline translation presentation exercise DI tests."""

import pytest

from contracts.aliases import CandidatesAlias
from di import MainContainer

from .._types.handler import (
    HandlerT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
)

# =================================================
# Tested handler
# =================================================


@pytest.fixture
def regular_presentation_handler(
    main_container: MainContainer,
) -> HandlerT:
    """Provide translation regular presentation exercise handler."""
    return (  # type: ignore
        main_container.lang.handlers.process_regular_translation_test()  # type: ignore
    )


@pytest.mark.django_db
def test_create_new_case(
    # Request parameters
    request_params: RequestParamsT,
    request_context: RequestContextT,
    request_data_create_task: RequestDataT,
    # Populate DB
    translation_candidates_db: CandidatesAlias,
    # Tested handler
    regular_presentation_handler: HandlerT,
) -> None:
    """Test that translations presentation exercise handler created."""
    # Act
    regular_presentation_handler.execute(
        request_params,
        request_context,
        request_data_create_task,
    )


def test_handler_initialized(
    regular_presentation_handler: HandlerT,
) -> None:
    """Test that presentation exercise handle initialized."""
    # Assert
    assert regular_presentation_handler is not None
