"""Glossary app types."""

from typing import TypedDict


class TermParamsType(TypedDict):
    """Fields type for Term study request."""

    category: list[str] | None
    marks: list[str] | None


class TermType(TypedDict):
    """Fields type for Term study response."""

    term: str
    definition: str
