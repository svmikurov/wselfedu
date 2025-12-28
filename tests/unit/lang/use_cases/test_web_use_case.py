"""Web get presentation UseCase tests."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from apps.lang import types, use_cases


@pytest.fixture
def mock_validator() -> Mock:
    """Provide validator mock."""
    return Mock(spec=types.Validator)


@pytest.fixture
def mock_service() -> Mock:
    """Provide business service mock."""
    return Mock(spec=types.BusinessService)


@pytest.fixture
def mock_response_adapter() -> Mock:
    """Provide response adapter mock."""
    return Mock(spec=types.ResponseAdapter)


class TestWebUseCase:
    """Web get presentation UseCase tests."""

    def test_initialize(
        self,
        mock_validator: Mock,
        mock_service: Mock,
        mock_response_adapter: Mock,
    ) -> None:
        """Web get presentation UseCase initialization."""
        # Act
        use_case = use_cases.WebPresentationUseCase(
            validator=mock_validator,
            service=mock_service,
            response_adapter=mock_response_adapter,
        )

        # Assert
        assert use_case is not None
