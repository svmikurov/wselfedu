"""Language rule response DTOs."""

from __future__ import annotations

from pydantic import Field

from apps.core.domains.base_dto import BaseDTO

# -------------------------------
# API Response DTO (external API)
# -------------------------------

# TODO: Add rule API Response DTO


# -------------------------------
# Web View DTO (template context)
# -------------------------------


class RuleClause(BaseDTO):
    """Rule clause with hierarchical structure."""

    pk: int
    content: str
    exception_note: str | None = None
    examples: str
    examples_for_practice: str
    exceptions: str
    exceptions_for_practice: str
    children: list[RuleClause] = Field(default_factory=list)


class LanguageRule(BaseDTO):
    """Complete language rule with clauses."""

    pk: int
    title: str
    clauses: list[RuleClause]
    rule_exceptions: str = Field(
        default='',
        examples=['child', 'man'],
        description='Rule-level exceptions',
    )
    practice_exceptions: str = Field(
        default='',
        examples=['child - children', 'man - men'],
        description='Exceptions for practice exercises',
    )
