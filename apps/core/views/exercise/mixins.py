"""Exercise view mixins."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Generic, TypeVar

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from contracts.schemas.base import NullDTO
from interfaces.protocols.request.general import RequestContextProtocol
from ports.contract.entity.general import NullProtocol
from ports.contract.enums.exercise import (
    ExerciseAction,
    ExerciseStatus,
)
from ports.contract.infra.handler import (
    RequestHandlerProtocol,
)
from ports.interfaces.protocols.web import RequestDataProtocol
from ports.interfaces.schemas.request.handler import (
    RequestContext,
    RequestData,
)
from ports.interfaces.schemas.response.web.base import HtmlResponseProtocol

from ..abstract import AbstractProcessAction, AbstractStartAction

if TYPE_CHECKING:
    from django.http import HttpRequest

ResponseDtoT = TypeVar(
    'ResponseDtoT',
    bound=HtmlResponseProtocol[ExerciseStatus],
)

HandlerT = TypeVar(
    'HandlerT',
    bound=RequestHandlerProtocol[
        NullProtocol,
        RequestContextProtocol,
        RequestDataProtocol[dict[str, str]],
        HtmlResponseProtocol[ExerciseStatus],
    ],
)

log = logging.getLogger(__name__)


PARTIAL_TEMPLATES: dict[ExerciseStatus, str] = {
    ExerciseStatus.NEW_TASK: '_new_case.html',
    ExerciseStatus.EXPLAIN: '_explain_case.html',
    ExerciseStatus.NO_CASE: '_no_case.html',
}
ERROR_TEMPLATE = '_case_request_error.html'


class ExercisePartialTemplateMixin(Generic[ResponseDtoT]):
    """Provides partial template for specific exercise status."""

    TEMPLATE_PATH: str

    def _get_partial_html(
        self,
        request: HttpRequest,
        schema: ResponseDtoT,
    ) -> str:
        """Get partial template html for exercise case."""
        try:
            template = PARTIAL_TEMPLATES[schema.domain_status]
            context = schema.context.model_dump()
        except KeyError as exc:
            log.exception(f'Get template key error: {exc}')
            template = ERROR_TEMPLATE
            context = {'error_message': _('Internal server error 500')}

        html = render_to_string(self.TEMPLATE_PATH + template, context)

        if request.headers.get('HX-Request'):
            return mark_safe(html + schema.html)

        return html


class StartExerciseMixin(
    AbstractStartAction[HtmlResponseProtocol[ExerciseStatus]],
):
    """Execute start exercise handler's action."""

    def _start(self, **kwargs: object) -> HtmlResponseProtocol[ExerciseStatus]:
        return self.handler.execute(  # type: ignore
            params=NullDTO(),
            context=RequestContext(user=self.user, is_htmx=self.is_htmx),  # type: ignore
            data=RequestData(data={'action': ExerciseAction.CREATE_TASK}),
        )


class ProcessExerciseMixin(
    AbstractProcessAction[HtmlResponseProtocol[ExerciseStatus]],
):
    """Execute process exercise handler's action."""

    request: HttpRequest

    def _process(
        self, **kwargs: object
    ) -> HtmlResponseProtocol[ExerciseStatus]:
        return self.handler.execute(  # type: ignore
            params=NullDTO(),
            context=RequestContext(user=self.user),  # type: ignore
            data=RequestData(data=self.request.POST.dict()),
        )


class ExerciseLoopMixin(StartExerciseMixin, ProcessExerciseMixin):
    """Loop exercise handler."""
