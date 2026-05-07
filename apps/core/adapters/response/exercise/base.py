"""Base WEB adapter."""

from abc import ABC, abstractmethod
from typing import Generic, TypeAlias, TypeVar, override

from django.template.loader import render_to_string

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from interfaces.schemas.web.task import PresentationTaskContext
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol

UseCaseResultT = TypeVar('UseCaseResultT')
ExtraContextT = TypeVar('ExtraContextT')
ResponseDataT = TypeVar('ResponseDataT')

HtmlT: TypeAlias = str
"""Partial HTML template.
"""


class BaseWebAdapter(
    BaseAuditable,
    AbstractResponseAdapter[UseCaseResultT, ExtraContextT, ResponseDataT],
    ABC,
    Generic[UseCaseResultT, ExtraContextT, ResponseDataT],
):
    """Base WEB adapter for perform exercise task.

    Returns response DTO.
    """

    def __init__(
        self,
        templates: tuple[HtmlT, ...],
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the adapter."""
        super().__init__(name=name, auditor=auditor)
        self._templates = templates

    def _get_html(self, context: PresentationTaskContext) -> HtmlT:
        """Build partial HTMLs."""
        html: list[str] = []
        for template in self.templates:
            html.append(render_to_string(template, context.model_dump()))
        return '\n'.join(html)

    @property
    def templates(self) -> tuple[HtmlT, ...]:
        """Return partial HTML templates."""
        return self._templates

    @override
    @abstractmethod
    def to_response(
        self,
        use_case_result: UseCaseResultT,
        request_context: ExtraContextT,
    ) -> ResponseDataT:
        """Convert domain schema to response representation."""
