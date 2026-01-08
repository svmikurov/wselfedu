"""Language application web adapter DTO."""

from pydantic import BaseModel


class ClauseSchema(BaseModel):
    """Language rule clauses web schema."""

    content: str
    examples: str
    exception_content: str | None
    exceptions: str


class RuleSchema(BaseModel):
    """Language rule web schema."""

    title: str
    clauses: list[ClauseSchema]
    exceptions: str
