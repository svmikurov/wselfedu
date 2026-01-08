"""Language rule web adapter."""

from django.db.models import QuerySet

from .. import models
from . import dto

# HACK: Refactor the web rule DTO building


class WebRuleAdapter:
    """Language rule web adapter."""

    @classmethod
    def to_response(cls, query: models.Rule) -> dto.RuleSchema:
        """Convert rule queryset to web representation context."""
        title = query.title
        clauses_qs = query.clauses
        exceptions_qs = query.exceptions

        clauses = []
        for clause in clauses_qs.all():
            examples, exceptions = [], []
            for item in clause.examples.all():
                if item.example_type == models.RuleExample.ExampleType.EXAMPLE:
                    examples.append(cls._create_example(item))
                elif (
                    item.example_type
                    == models.RuleExample.ExampleType.EXCEPTION
                ):
                    exceptions.append(cls._create_example(item))

            clauses.append(
                dto.ClauseSchema(
                    content=clause.content,
                    examples=cls._join_examples(examples),
                    exception_content=clause.exception_content,
                    exceptions=cls._join_examples(exceptions),
                )
            )

        return dto.RuleSchema(
            title=title,
            clauses=clauses,
            exceptions=cls._build_examples_string(exceptions_qs),
        )

    @classmethod
    def _build_examples_string(cls, examples: QuerySet[models.Rule]) -> str:
        examples = [cls._create_example(item) for item in examples.all()]

        return cls._join_examples(examples)

    @staticmethod
    def _create_example(example: QuerySet[models.Rule]) -> str:
        return (
            f'{example.question_translation.english} - '
            f'{example.answer_translation.english}'
        )

    @staticmethod
    def _join_examples(items: list[str]) -> str:
        example_count = 5
        return ', '.join(items[:example_count])
