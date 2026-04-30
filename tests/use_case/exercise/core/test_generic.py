"""Generic exercise use case tests."""

from unittest.mock import Mock

from apps.users.models import Person

from ._types import CommandT, UseCaseT
from .conftest import STORE_PREFIX

# TODO: Add tests for other cases
# TODO: Update type hint from `Mock` to aliases


def test_execute_new_case_command(
    mock_user: Person,
    # DTOs
    create_command: CommandT,
    mock_params: Mock,
    mock_spec: Mock,
    mock_case: Mock,
    domain_result: Mock,
    # Use case's dependencies
    mock_empty_storage: Mock,
    mock_create_adapter: Mock,
    mock_create_service: Mock,
    mock_create_builder: Mock,
    # Use case
    use_case: UseCaseT,
) -> None:
    """Test that exercise use case returns result."""
    # Act
    use_case.execute(create_command)

    # Assert
    mock_empty_storage.retrieve.assert_called_once_with(
        create_command,
        STORE_PREFIX,
    )
    mock_create_adapter.adapt.assert_called_once_with(
        create_command,
        mock_params,
        None,
    )
    mock_create_service.execute.assert_called_once_with(
        mock_user,
        mock_spec,
    )
    mock_create_builder.build.assert_called_once_with(
        mock_case,
        mock_spec,
    )
    mock_empty_storage.save.assert_called_once_with(
        create_command,
        domain_result,
        STORE_PREFIX,
    )
    mock_create_builder.build.assert_called_once_with(
        mock_case,
        mock_spec,
    )


def test_execute_successfully(
    create_command: CommandT,
    use_case: UseCaseT,
    mock_use_case_result: Mock,
) -> None:
    """Test that use case execute was completed successfully."""
    # Act & Assert
    assert use_case.execute(create_command) == mock_use_case_result


def test_use_case_initialized(
    use_case: UseCaseT,
) -> None:
    """Test that exercise use case initialized successfully."""
    # Assert
    assert use_case is not None
