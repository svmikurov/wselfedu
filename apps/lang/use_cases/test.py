"""Language discipline test exercise UseCase."""

from typing import Any

from ..schemas import (
    Case,
    DetailTestRequestDTO,
    Explanation,
    TestRequestDTO,
    TestResponseData,
)
from . import DetailUseCase, UseCase

type RequestData = dict[str, Any]
type DomainResult = Case | Explanation


class WebTestUseCase(
    UseCase[RequestData, TestRequestDTO, DomainResult, TestResponseData]
):
    """Web translation study test exercise UseCase."""


class AssignmentUseCase(
    DetailUseCase[
        RequestData, DetailTestRequestDTO, DomainResult, TestResponseData
    ]
):
    """Web translation test exercise UseCase with assignment ID."""
