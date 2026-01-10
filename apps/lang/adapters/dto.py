"""Language application web adapter DTO."""

from __future__ import annotations

from pydantic import BaseModel


class ClauseSchema(BaseModel):
    """Language rule clauses web schema."""

    id: int
    content: str
    examples: str
    exception_content: str | None
    exceptions: str

    children: list[ClauseSchema]


class RuleSchema(BaseModel):
    """Language rule web schema."""

    id: int
    title: str
    clauses: list[ClauseSchema]
    exceptions: str
