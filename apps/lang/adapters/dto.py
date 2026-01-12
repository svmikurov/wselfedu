"""Language application web adapter DTO."""

from __future__ import annotations

from pydantic import BaseModel


class ClauseSchema(BaseModel):
    """Language rule clauses web schema."""

    id: int
    content: str
    exception_content: str | None
    examples: str
    task_examples: str
    exceptions: str
    task_exceptions: str

    children: list[ClauseSchema]


class RuleSchema(BaseModel):
    """Language rule web schema."""

    id: int
    title: str
    clauses: list[ClauseSchema]
    exceptions: str
    task_exceptions: str
