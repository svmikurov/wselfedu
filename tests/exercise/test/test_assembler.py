"""Exercise request handler command tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from kernel.assembler.impl import UserDataAssembler

if TYPE_CHECKING:
    from interfaces.protocols.request.general import RequestContextProtocol
    from ports.contract.entity.general import NullProtocol
    from ports.interfaces.protocols.command.assembler import AssemblerProtocol
    from ports.interfaces.protocols.command.exercise import (
        CheckTestCommandProtocol,
        CreateTaskCommandProtocol,
    )
    from tests.types.handler import RequestContextT, RequestParamsT

    from .._types import (
        ValidatedCheckT,
        ValidatedCreateT,
    )

    # Assembler types
    type AssemblerT = AssemblerProtocol[
        NullProtocol,
        RequestContextProtocol,
        ValidatedCreateT,
        Any,
    ]
    type CheckAssemblerT = AssemblerProtocol[
        NullProtocol,
        RequestContextProtocol,
        ValidatedCheckT,
        Any,
    ]


# =================================================
# Fixtures
# =================================================


@pytest.fixture
def assembler() -> AssemblerT:
    """Provide request handler command assembler."""
    return UserDataAssembler()


# =================================================
# Tests
# =================================================


@pytest.mark.django_db
def test_create_command(
    mock_request_params: RequestParamsT,
    request_context: RequestContextT,
    validated_create: ValidatedCreateT,
    assembler: AssemblerT,
    create_task_command: CreateTaskCommandProtocol,
) -> None:
    """Create exercise task command test."""
    assert (
        assembler.prepare(
            mock_request_params,
            request_context,
            validated_create,
        )
        == create_task_command
    )


@pytest.mark.django_db
def test_check_command(
    mock_request_params: RequestParamsT,
    request_context: RequestContextT,
    validated_check: ValidatedCreateT,
    assembler: AssemblerT,
    check_test_command: CheckTestCommandProtocol,
) -> None:
    """Create exercise task command test."""
    assert (
        assembler.prepare(
            mock_request_params,
            request_context,
            validated_check,
        )
        == check_test_command
    )
