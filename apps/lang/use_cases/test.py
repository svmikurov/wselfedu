"""Language discipline test exercise UseCase."""

from typing import Any

from .. import schemas
from . import BaseUseCase

type RequestData = dict[str, Any]


class WebTestUseCase(
    BaseUseCase[
        RequestData,
        schemas.TestRequestDTO,
        schemas.Case | schemas.Explanation,
        schemas.TestResponseData,
    ]
):
    """Web translation study test exercise UseCase."""
