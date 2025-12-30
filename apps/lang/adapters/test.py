"""Test exercise adapters."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..schemas.test import (
    Case,
    CaseStatus,
    Explanation,
    TestResponseData,
)

if TYPE_CHECKING:
    from ..schemas import Case, Explanation


class WebTestAdapter:
    """Web test exercise response adapter.

    Converts domain data to web-ready format.
    """

    @classmethod
    def to_response(cls, case: Case | Explanation) -> TestResponseData:
        """Convert domain result to web representation context."""
        match case.status:
            case CaseStatus.NEW:
                data = Case(**case.model_dump())

            case CaseStatus.EXPLANATION:
                data = Explanation(**case.model_dump())  # type: ignore[assignment]

            case _:
                raise ValueError('Unsupported case status')

        return TestResponseData(status=case.status, data=data)
