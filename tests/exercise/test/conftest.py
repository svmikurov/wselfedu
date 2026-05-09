"""Exercise test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.core.handlers.dto import RequestData
from contracts.enums import ExerciseAction
from interfaces.schemas.validator.task import (
    ValidatedCheckTestAnswer,
    ValidatedCreateTask,
)

if TYPE_CHECKING:
    from .._types import (
        CheckRequestDataT,
        CreateRequestDataT,
        ValidatedCheckT,
        ValidatedCreateT,
    )


# =================================================
# Request data
# =================================================


@pytest.fixture
def create_request_data() -> CreateRequestDataT:
    """Provide create exercise request's data DTO."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': ExerciseAction.CREATE_TASK,
        },
    )


@pytest.fixture
def check_request_data() -> CheckRequestDataT:
    """Provide check exercise request's data DTO."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': ExerciseAction.CHECK_ANSWER,
            'option_value': '3',
        },
    )


# =================================================
# Validated data
# =================================================


@pytest.fixture
def validated_create() -> ValidatedCreateT:
    """Provide the *create task* DTO validated request data."""
    return ValidatedCreateTask(
        action=ExerciseAction.CREATE_TASK,
    )


@pytest.fixture
def validated_check() -> ValidatedCheckT:
    """Provide the *check test answer* DTO validated request data."""
    return ValidatedCheckTestAnswer(
        action=ExerciseAction.CHECK_ANSWER,
        option_value=3,
    )
