"""Glossary app types."""

from typing import TypedDict


class ParamsType(TypedDict):
    """Fields type for Terms study exercise."""

    category: list[str] | None
    marks: list[str] | None


class QuestionType(TypedDict):
    """Fields type for Terms study exercise."""

    term: str
    definition: str
