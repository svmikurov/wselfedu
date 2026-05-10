"""Abstract base classes for response adapter."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from ports.contract.infra.adapter import AdapterProtocol

UseCaseResultT = TypeVar('UseCaseResultT')
ExtraContextT = TypeVar('ExtraContextT')
ResponseDataT = TypeVar('ResponseDataT')


class AbstractResponseAdapter(
    ABC,
    AdapterProtocol[
        UseCaseResultT,
        ExtraContextT,
        ResponseDataT,
    ],
):
    """ABC for response adapter.

    Converts domain DTO to Web response format.
    Includes extra context needed for server-rendered templates.
    """

    @override
    @abstractmethod
    def to_response(
        self,
        use_case_result: UseCaseResultT,
        request_context: ExtraContextT,
    ) -> ResponseDataT:
        """Convert domain schema to response representation."""

    @property
    def name(self) -> str:
        """Return adapter name."""
        return self._name  # type: ignore
