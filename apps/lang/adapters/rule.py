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
                    examples.append(cls._build_example(item))
                elif (
                    item.example_type
                    == models.RuleExample.ExampleType.EXCEPTION
                ):
                    exceptions.append(cls._build_example(item))

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
            exceptions=cls._convert_examples(exceptions_qs.all()),
        )

    @classmethod
    def _convert_examples(
        cls,
        examples: QuerySet[models.RuleExample] | QuerySet[models.RuleExample],
    ) -> str:
        """Convert rule examples/exceptions queryset to string."""
        examples = [cls._build_example(item) for item in examples]  # type: ignore[assignment]
        result = cls._join_examples(examples)  # type: ignore[arg-type]
        return result

    @staticmethod
    def _build_example(
        example: models.RuleExample | models.RuleException,
    ) -> str:
        """Build a string representation of the example/exception."""
        return (
            f'{example.question_translation.english} - '
            f'{example.answer_translation.english}'
        )

    @staticmethod
    def _join_examples(items: list[str]) -> str:
        """Combine examples/exceptions into a string representation."""
        example_count = 5
        return ', '.join(items[:example_count])
