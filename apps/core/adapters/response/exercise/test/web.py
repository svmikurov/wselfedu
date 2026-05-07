"""Test exercise response adapters."""

from typing import Any, Iterable, TypeVar, override

from django.template.loader import render_to_string

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from apps.core.adapters.response.status import ResponseStatusEnum
from apps.core.domains.exercise.test.dto import TestExerciseCase
from contracts import NullProtocol
from contracts.entity.domain.exercise.fields import ExerciseCaseProtocol
from contracts.entity.response.base import HtmlResponseProtocol
from contracts.schemas.domain.exercise.flow import TestExerciseTask
from contracts.schemas.response.generic import HtmlResponseDTO
from interfaces.schemas.web.task import (
    Option,
    TestExerciseTaskResponse,
    TestTaskContext,
)

from ..base import BaseWebAdapter

ExtraContextT = TypeVar('ExtraContextT', bound=Iterable[Any])


class WebTestExerciseAdapter(
    BaseWebAdapter[
        ExerciseCaseProtocol[TestExerciseTask[list[Option]]],
        NullProtocol,
        TestExerciseTaskResponse,
    ],
):
    """Web test exercise response adapter."""

    # HACK: Update return type hint on protocol
    @override
    def to_response(
        self,
        # FIXME: Fix type hint
        domain_result: ExerciseCaseProtocol[TestExerciseTask[list[Option]]],
        request_context: NullProtocol,
    ) -> TestExerciseTaskResponse:
        """Convert domain result to web representation context."""
        context = TestTaskContext(
            question_text=domain_result.domain.items[
                domain_result.domain.question_option_value
            ].text,
            options=domain_result.domain.items,
        )
        return TestExerciseTaskResponse(
            domain_status=domain_result.status,
            context=context,
        )


# QUESTION: Is deprecated the web explain adapter
class WebExplainAdapter(
    AbstractResponseAdapter[
        TestExerciseCase[ExtraContextT],
        NullProtocol,
        HtmlResponseProtocol[TestExerciseCase[ExtraContextT]],
    ],
):
    """Web test exercise explain response adapter.

    Returns response DTO.
    """

    def __init__(
        self,
        extra_templates: list[str],
    ) -> None:
        """Construct the adapter."""
        self._templates = extra_templates

    def _build_html(
        self,
        domain_result: TestExerciseCase[ExtraContextT],
    ) -> str:
        """Build HTML."""
        html = ''
        for template in self._templates:
            html += render_to_string(template, domain_result.model_dump())
        return html

    @override
    def to_response(
        self,
        domain_result: TestExerciseCase[ExtraContextT],
        request_context: NullProtocol,
    ) -> HtmlResponseProtocol[TestExerciseCase[ExtraContextT]]:
        """Convert domain result to web representation context."""
        return HtmlResponseDTO(
            domain_status=ResponseStatusEnum.EXPLAIN_CASE,  # type: ignore
            context=TestTaskContext(
                question_text=domain_result.question_text,
                options=[
                    Option(
                        value=option.options_value,
                        text=option.text,
                    )
                    for option in domain_result.items
                ],
            ),
            html=self._build_html(domain_result),
        )
