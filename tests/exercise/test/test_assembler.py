"""Exercise request handler command tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from apps.core.assemblers.impl import UserDataAssembler

if TYPE_CHECKING:
    from apps.core.assemblers.protocol import AssemblerProtocol
    from contracts.entity.general import NullProtocol
    from interfaces.protocols.request.general import RequestContextProtocol
    from tests.types.handler import RequestContextT, RequestParamsT

    from .._types import (
        ValidatedCheckT,
        ValidatedCreateT,
    )

    # Assembler types
    type CreateAssemblerT = AssemblerProtocol[
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
def assembler() -> CreateAssemblerT:
    """Provide request handler command assembler."""
    return UserDataAssembler()


# =================================================
# Tests
# =================================================


@pytest.mark.django_db
def test_create_command(
    request_params: RequestParamsT,
    request_context: RequestContextT,
    create_task_request_data: ValidatedCreateT,
    assembler: CreateAssemblerT,
) -> None:
    """Create exercise task command test."""
    assembler.prepare(
        request_params,
        request_context,
        create_task_request_data,
    )
