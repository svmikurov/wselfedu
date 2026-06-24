"""Protocols for Django site interface."""

from typing import Any, Protocol


class HasHtml(Protocol):
    @property
    def html(self) -> str: ...


class HasDataContext(Protocol):
    @property
    def context(self) -> dict[str, Any]: ...


class HtmlResponsible(
    HasHtml,
    HasDataContext,
    Protocol,
): ...
