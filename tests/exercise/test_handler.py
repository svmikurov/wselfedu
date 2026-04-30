"""Language discipline translation presentation exercise DI tests."""

import pytest

from contracts.aliases import CandidatesAlias

from .._types.handler import (
    HandlerT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
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
