"""Regular translation presentation handler tests."""

import pytest

from di import MainContainer

from .._types import (
    HandlerT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
    TranslationsT,
)


@pytest.fixture
def handler(main_container: MainContainer) -> HandlerT:
    """Provide regular translation presentation DI handler."""
    return (  # type: ignore
        main_container.lang.handlers.regular_translation_presentation()  # type: ignore
    )


def test_initialize(handler: HandlerT) -> None:
    """Test that handler initialized successfully."""
    assert handler is not None


@pytest.mark.django_db
def test_create_task(
    handler: HandlerT,
    null_request_params: RequestParamsT,
    user_request_context: RequestContextT,
    create_request_data: RequestDataT,
    translations: TranslationsT,  # Populate DB
) -> None:
    """Test *create task* action completed successfully."""
    # Act & Assert
    assert (
        handler.execute(
            null_request_params,
            user_request_context,
            create_request_data,
        )
        is not None
    )


@pytest.mark.django_db
def test_update_progress(
    handler: HandlerT,
    null_request_params: RequestParamsT,
    user_request_context: RequestContextT,
    update_progress_request_data: RequestDataT,
    translations: TranslationsT,  # Populate DB
) -> None:
    """Test *update progress* action completed successfully."""
    # Act & Assert
    assert (
        handler.execute(
            null_request_params,
            user_request_context,
            update_progress_request_data,
        )
        is not None
    )
