"""Language rule web adapter."""

from typing import Any

from django.db.models import QuerySet

from .. import models
from . import WebRuleAdapterABC, dto


class WebRuleAdapter(WebRuleAdapterABC):
    """Language rule web adapter."""

    EXAMPLE_COUNT: int | None = 5

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Construct the adapter."""
        self._config = config if config else {}

    def to_response(self, query: models.Rule) -> dto.RuleSchema:
        """Get clauses DTO with clause examples/exceptions."""
        clauses_qs: QuerySet[models.RuleClause] = query.clauses.all()
        exceptions_qs: QuerySet[models.RuleException] = query.exceptions.all()

        # If clause is child it has parent ID, else parent ID is `None`
        parent_mapping: dict[int | None, list[models.RuleClause]] = {}

        for clause in clauses_qs:
            parent_mapping.setdefault(
                clause.parent.pk if clause.parent else None, []
            ).append(clause)

        root_clauses: list[dto.ClauseSchema] = []
        for clause in parent_mapping.get(None, []):
            children: list[dto.ClauseSchema] = []

            for child in parent_mapping.get(clause.pk, []):
                if child:
                    children.append(self._build_clause_dto(child))

            root_clauses.append(self._build_clause_dto(clause, children))

        rule_dto = dto.RuleSchema(
            id=query.pk,
            title=query.title,
            clauses=root_clauses,
            exceptions=self._convert_exceptions(exceptions_qs),
            task_exceptions=self._convert_examples(exceptions_qs),
        )
        return rule_dto

    # ----------------------------------------------------------
    # Converting an example/exception to a string representation
    # ----------------------------------------------------------

    def _convert_exceptions(
        self, exception_qs: QuerySet[models.RuleException]
    ) -> str:
        """Convert rule exceptions queryset to string."""
        exceptions = [exc.question_in_foreign for exc in exception_qs]
        return self._to_string(exceptions)

    def _convert_examples(
        self,
        examples_qs: QuerySet[models.RuleTaskExample]
        | QuerySet[models.RuleException],
    ) -> str:
        """Convert rule task examples/exceptions queryset to string."""
        examples = [example.task for example in examples_qs]
        return self._to_string(examples)

    def _to_string(self, items: list[str]) -> str:
        """Combine examples/exceptions into a string representation."""
        example_count = self._config.get('example_count', self.EXAMPLE_COUNT)
        if example_count:
            return ', '.join(items[:example_count])
        return ', '.join(items)

    # ----------------------------
    # Getting an example/exception
    # ----------------------------

    def _get_examples(
        self, examples_qs: QuerySet[models.RuleExample]
    ) -> tuple[list[str], list[str]]:
        """Get clause examples/exceptions."""
        examples: list[str] = []
        exceptions: list[str] = []

        for example in examples_qs:
            if example.example_type == models.ExampleType.EXAMPLE:
                examples.append(example.question_in_foreign)
            elif example.example_type == models.ExampleType.EXCEPTION:
                exceptions.append(example.question_in_foreign)

        return examples, exceptions

    def _get_task_examples(
        self, examples_qs: QuerySet[models.RuleTaskExample]
    ) -> tuple[list[str], list[str]]:
        """Get clause task examples/exceptions."""
        examples: list[str] = []
        exceptions: list[str] = []

        for example in examples_qs:
            if example.example_type == models.ExampleType.EXAMPLE:
                examples.append(example.task)
            elif example.example_type == models.ExampleType.EXCEPTION:
                exceptions.append(example.task)

        return examples, exceptions

    # ------------
    # DTO building
    # ------------

    def _build_clause_dto(
        self,
        clause: models.RuleClause,
        children: list[dto.ClauseSchema] | None = None,
    ) -> dto.ClauseSchema:
        """Build clause DTO."""
        # Rule clause task examples/exceptions
        task_examples, task_exceptions = self._get_task_examples(
            clause.rule_task_examples.all()
        )
        # Rule clause translation examples/exceptions
        examples, exceptions = self._get_examples(
            clause.rule_translation_examples.all()
        )
        return dto.ClauseSchema(
            id=clause.pk,
            content=clause.content,
            exception_content=clause.exception_content,
            examples=self._to_string(examples),
            task_examples=self._to_string(task_examples),
            exceptions=self._to_string(exceptions),
            task_exceptions=self._to_string(task_exceptions),
            children=children if children is not None else [],
        )
