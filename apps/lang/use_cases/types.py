"""UseCase type hints."""

from typing import Any, TypeAlias

from .. import schemas
from .generic import DetailUseCase, UseCase

# Type aliases for request/response data
type RequestData = dict[str, Any]
type DomainResult = schemas.Case | schemas.Explanation

# -------------------------------
# Test exercise UseCase type hint
# -------------------------------


WebTest: TypeAlias = UseCase[
    RequestData,
    schemas.TestRequestDTO,
    DomainResult,
    schemas.TestResponseData,
]
"""UseCase for regular web translation study tests."""

WebAssignedTest: TypeAlias = DetailUseCase[
    RequestData,
    schemas.DetailTestRequestDTO,
    DomainResult,
    schemas.TestResponseData,
]
"""UseCase for web translation tests with assignment pk."""
