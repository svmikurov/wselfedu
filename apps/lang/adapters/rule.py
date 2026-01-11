"""Language rule web adapter."""

from typing import Any

from django.db.models import QuerySet

from .. import models
from . import WebRuleAdapterABC, dto

# TODO: Refactor this code


class WebRuleAdapter(WebRuleAdapterABC):
    """Language rule web adapter."""

    EXAMPLE_COUNT: int | None = 5

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Construct the adapter."""
        self._config = config if config else {}

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
                    children.append(self._build_clause_dto(child))

            clauses.append(self._build_clause_dto(clause, children))

        rule_dto = dto.RuleSchema(
            id=query.pk,
            title=query.title,
            clauses=clauses,
            exceptions=self._convert_task_examples(query.exceptions.all()),  # type: ignore[arg-type]
            task_exceptions=self._convert_task_examples(
                query.exceptions.all()
            ),  # type: ignore[arg-type]
        )
        return rule_dto

    def _convert_examples(
        self,
        examples: QuerySet[models.RuleExample]
        | QuerySet[models.RuleException],
    ) -> str:
        """Convert rule examples/exceptions queryset to string."""
        examples = [self._build_example(item) for item in examples]  # type: ignore[assignment]
        result = self._join_examples(examples)  # type: ignore[arg-type]
        return result

    def _convert_task_examples(
        self,
        examples: QuerySet[models.RuleTaskExample]
        | QuerySet[models.RuleTaskExample],
    ) -> str:
        """Convert rule task examples/exceptions queryset to string."""
        examples = [self._build_task_example(item) for item in examples]  # type: ignore[assignment]
        result = self._join_examples(examples)  # type: ignore[arg-type]
        return result

    @staticmethod
    def _build_example(
        example: models.RuleExample | models.RuleException,
    ) -> str:
        """Return a word example/exception."""
        return example.translation.foreign.word

    @staticmethod
    def _build_task_example(
        example: models.RuleTaskExample | models.RuleException,
    ) -> str:
        """Build a string repr of the task example/exception."""
        return (
            f'{example.question_translation.foreign} - '
            f'{example.answer_translation.foreign}'
        )

    def _join_examples(self, items: list[str]) -> str:
        """Combine examples/exceptions into a string representation."""
        example_count = self._config.get('example_count', self.EXAMPLE_COUNT)
        if example_count:
            return ', '.join(items[:example_count])
        return ', '.join(items)

    def _get_examples(
        self,
        examples_qs: QuerySet[models.RuleTaskExample]
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

    def _get_task_examples(
        self,
        examples_qs: QuerySet[models.RuleTaskExample]
        | QuerySet[models.RuleException],
    ) -> tuple[list[str], list[str]]:
        """Get clause task examples with exceptions."""
        examples: list[str] = []
        exceptions: list[str] = []

        for instance in examples_qs:
            if (
                instance.example_type  # type: ignore[union-attr]:
                == models.RuleTaskExample.ExampleType.EXAMPLE
            ):
                examples.append(self._build_task_example(instance))

            elif (
                instance.example_type  # type: ignore[union-attr]
                == models.RuleTaskExample.ExampleType.EXCEPTION
            ):
                exceptions.append(self._build_task_example(instance))

        return examples, exceptions

    def _build_clause_dto(
        self,
        clause: models.RuleClause,
        children: list[dto.ClauseSchema] | None = None,
    ) -> dto.ClauseSchema:
        """Build clause DTO."""
        # Rule clause task examples & exceptions
        task_examples, task_exceptions = self._get_task_examples(
            clause.rule_task_examples.all()
        )
        # Rule clause translation examples & exceptions
        examples, exceptions = self._get_examples(
            clause.rule_translation_examples.all()
        )
        return dto.ClauseSchema(
            id=clause.pk,
            content=clause.content,
            exception_content=clause.exception_content,
            examples=self._join_examples(examples),
            task_examples=self._join_examples(task_examples),
            exceptions=self._join_examples(exceptions),
            task_exceptions=self._join_examples(task_exceptions),
            children=children if children is not None else [],
        )
