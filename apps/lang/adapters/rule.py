"""Language rule web adapter."""

from typing import Any

from django.db.models import QuerySet

from .. import models
from . import WebRuleAdapterABC, dto


class WebRuleAdapter(WebRuleAdapterABC):
    """Language rule web adapter."""

    example_count = 5

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Construct the adapter."""
        self._config = config if config else {}

    def _convert_examples(
        self,
        examples: QuerySet[models.RuleExample] | QuerySet[models.RuleExample],
    ) -> str:
        """Convert rule examples/exceptions queryset to string."""
        examples = [self._build_example(item) for item in examples]  # type: ignore[assignment]
        result = self._join_examples(examples)  # type: ignore[arg-type]
        return result

    @staticmethod
    def _build_example(
        example: models.RuleExample | models.RuleException,
    ) -> str:
        """Build a string representation of the example/exception."""
        return (
            f'{example.question_translation.foreign} - '
            f'{example.answer_translation.foreign}'
        )

    def _join_examples(self, items: list[str]) -> str:
        """Combine examples/exceptions into a string representation."""
        example_count = self._config.get('example_count', self.example_count)
        return ', '.join(items[:example_count])

    def _get_examples(
        self,
        examples_qs: QuerySet[models.RuleExample]
        | QuerySet[models.RuleException],
    ) -> tuple[list[str], list[str]]:
        """Get clause examples with exceptions."""
        examples: list[str] = []
        exceptions: list[str] = []

        for instance in examples_qs:
            if instance.example_type == models.RuleExample.ExampleType.EXAMPLE:  # type: ignore[union-attr]
                examples.append(self._build_example(instance))
            elif (
                instance.example_type  # type: ignore[union-attr]
                == models.RuleExample.ExampleType.EXCEPTION
            ):
                exceptions.append(self._build_example(instance))

        return examples, exceptions

    def to_response(self, query: models.Rule) -> dto.RuleSchema:
        """Get nested DTO."""
        clauses_qs: QuerySet[models.RuleClause] = query.clauses.all()
        mapping: dict[int | None, list[models.RuleClause]] = {}

        for clause in clauses_qs:
            mapping.setdefault(
                clause.parent.pk if clause.parent else None, []
            ).append(clause)

        clauses: list[dto.ClauseSchema] = []
        for clause in mapping.get(None, []):
            children: list[dto.ClauseSchema] = []

            for child in mapping.get(clause.pk, []):
                if child:
                    children.append(self.build_clause_dto(child))

            clauses.append(self.build_clause_dto(clause, children))

        return dto.RuleSchema(
            id=query.pk,
            title=query.title,
            clauses=clauses,
            exceptions=self._convert_examples(query.exceptions.all()),  # type: ignore[arg-type]
        )

    def build_clause_dto(
        self,
        clause: models.RuleClause,
        children: list[dto.ClauseSchema] | None = None,
    ) -> dto.ClauseSchema:
        """Build clause DTO."""
        examples, exceptions = self._get_examples(clause.examples.all())
        return dto.ClauseSchema(
            id=clause.pk,
            content=clause.content,
            examples=self._join_examples(examples),
            exception_content=clause.exception_content,
            exceptions=self._join_examples(exceptions),
            children=children if children is not None else [],
        )
