"""Application layer request handler result adapter."""

from typing import Iterable, TypeAlias

from django.template.loader import render_to_string

from wse.application.protocols import HasTask
from wse.domain.protocols import Testable

from .. import dto
from ..interfaces.protocols import HasContext, HasHtml, HasIsHtmx, NullProto
from ..interfaces.response import (
    CreateTestingTaskContext,
)
from .abstract import AbstractAdapter

HtmlT: TypeAlias = str
"""Partial HTML template.
"""


class NullAdapter(
    AbstractAdapter[NullProto, NullProto, NullProto],
):
    """Null adapter."""

    def to_response(self, source: NullProto, context: NullProto) -> NullProto:
        """Return original data."""
        return source


class CreateTestingAdapter(
    AbstractAdapter[
        HasTask[Testable],
        HasIsHtmx,
        HasContext[CreateTestingTaskContext],
    ],
):
    """Adapter for create testing task web response context."""

    def __init__(
        self,
        templates: Iterable[str],
    ) -> None:
        """Construct the adapter."""
        super().__init__()
        self._templates = templates

    def _get_html(self, context: CreateTestingTaskContext) -> HtmlT:
        """Build partial HTMLs."""
        html: list[str] = []
        for template in self._templates:
            html.append(render_to_string(template, context))
        return '\n'.join(html)

    def to_response(
        self,
        source: HasTask[Testable],
        request_context: HasIsHtmx,
    ) -> HasContext[CreateTestingTaskContext]:
        """Adapt for web response context."""
        response_context: CreateTestingTaskContext = {
            'question_text': source.task.question_text,
            'options': [
                {
                    'value': option.option_value,
                    'text': option.option_text,
                }
                for option in source.task.options
            ],
        }
        html = (
            self._get_html(response_context) if request_context.is_htmx else ''
        )
        return dto.ResponseDto(response_context, html)


class CheckTestingAdapter(
    AbstractAdapter[
        NullProto,
        NullProto,
        HasHtml,
    ]
):
    """Adapter for check testing task web response context."""

    def to_response(
        self,
        source: NullProto,
        context: NullProto,
    ) -> HasHtml:
        """Adapt a testing answer check result for web response."""
        # HACK: Implement result context rendering
        return dto.ResponseDto(
            context={},
        )
