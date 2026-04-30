"""Discipline rule response DTOs."""

from __future__ import annotations

from pydantic import Field

from contracts.schemas.base import BaseDTO


class RuleClauseDTO(BaseDTO):
    """Rule clause with hierarchical structure DTO."""

    pk: int
    content: str
    exception_note: str | None = None
    examples: str
    examples_for_practice: str
    exceptions: str
    exceptions_for_practice: str
    children: list[RuleClauseDTO] = Field(default_factory=list)


class RuleDTO(BaseDTO):
    """Rule with clauses DTO."""

    pk: int
    title: str
    clauses: list[RuleClauseDTO]
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
