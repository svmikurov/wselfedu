"""Language rule web adapter."""

from ..models import Rule, RuleExample
from typing import Any
from pydantic import BaseModel
from django.db.models import QuerySet

# HACK: Refactor the web rule DTO building


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


class WebRuleAdapter:
    """Language rule web adapter."""

    @classmethod
    def to_response(cls, query: Rule) -> RuleSchema:
        """Convert rule queryset to web representation context."""

        title = query.title
        clauses_qs = query.clauses
        exceptions_qs = query.exceptions

        clauses = []
        for clause in clauses_qs.all():
            
            examples, exceptions = [], []
            for item in clause.examples.all():
                if item.example_type == RuleExample.ExampleType.EXAMPLE:
                    examples.append(cls._create_example(item))
                elif item.example_type == RuleExample.ExampleType.EXCEPTION:
                    exceptions.append(cls._create_example(item))

            clauses.append(
                ClauseSchema(
                    content=clause.content,
                    examples=cls._join_examples(examples),
                    exception_content=clause.exception_content,
                    exceptions=cls._join_examples(exceptions),
                )
            )
            
        return RuleSchema(
            title=title,
            clauses=clauses,
            exceptions=cls._build_examples_string(exceptions_qs)
        )

    @classmethod
    def _build_examples_string(cls, examples: QuerySet[Any]) -> str:
        examples = [cls._create_example(item) for item in examples.all()]

        return cls._join_examples(examples)

    @staticmethod
    def _create_example(example: QuerySet[Any]) -> str:
        return f'{example.question_translation.english} - {example.answer_translation.english}'
    
    @staticmethod
    def _join_examples(items: list[str]) -> str:
        count = 5
        return ', '.join(items[:count])