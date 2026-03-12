"""Regular request handler tests."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from apps.core.handlers import RegularRequestHandler
from apps.core.handlers.protocol import (
    DataUseCaseProtocol,
    GenericAdapterProtocol,
    ValidatorProtocol,
)


@pytest.fixture
def mock_validator() -> Mock:
    """Provide validator mock."""
    return Mock(spec=ValidatorProtocol)


@pytest.fixture
def mock_service() -> Mock:
    """Provide business service mock."""
    return Mock(spec=DataUseCaseProtocol)


@pytest.fixture
def mock_response_adapter() -> Mock:
    """Provide response adapter mock."""
    return Mock(spec=GenericAdapterProtocol)


class TestRegularRequestHandler:
    """Web regular request handler test."""

    def test_initialize(
        self,
        mock_validator: Mock,
        mock_service: Mock,
        mock_response_adapter: Mock,
    ) -> None:
        """Web get presentation UseCase initialization."""
        # Act
        handler = RegularRequestHandler(  # type: ignore[var-annotated]
            validator=mock_validator,
            use_case=mock_service,
            adapter=mock_response_adapter,
        )

        # Assert
        assert handler is not None
