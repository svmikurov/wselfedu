"""Api get presentation UseCase tests."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from apps.lang.types import presentation
from apps.lang.use_cases import ApiPresentationUseCase


@pytest.fixture
def mock_service() -> Mock:
    """Provide business service mock."""
    return Mock(spec=presentation.BusinessService)


@pytest.fixture
def mock_validator() -> Mock:
    """Provide validator mock."""
    return Mock(spec=presentation.Validator)


@pytest.fixture
def mock_response_adapter() -> Mock:
    """Provide response adapter mock."""
    return Mock(spec=presentation.ResponseAdapter)


class TestWebUseCase:
    """Api get presentation UseCase tests."""

    def test_initialize(
        self,
        mock_validator: Mock,
        mock_service: Mock,
        mock_response_adapter: Mock,
    ) -> None:
        """Api get presentation UseCase initialization."""
        # Act
        use_case = ApiPresentationUseCase(
            validator=mock_validator,
            service=mock_service,
            response_adapter=mock_response_adapter,
        )

        # Assert
        assert use_case is not None
