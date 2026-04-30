"""Exercise view mixins."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Generic, TypeVar

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from apps.core.handlers.dto import RequestContext, RequestData
from apps.core.handlers.protocol import (
    RequestContextProtocol,
    RequestDataProtocol,
    RequestHandlerProtocol,
)
from contracts.entity.general import NullProtocol
from contracts.entity.response.base import OobResponseProtocol
from contracts.enums.exercise import (
    ExerciseAction,
    ExerciseStatus,
)
from contracts.schemas.base import NullDTO

from ..abstract import AbstractProcessAction, AbstractStartAction

if TYPE_CHECKING:
    from django.http import HttpRequest

ResponseDtoT = TypeVar(
    'ResponseDtoT',
    bound=OobResponseProtocol[ExerciseStatus],
)

HandlerT = TypeVar(
    'HandlerT',
    bound=RequestHandlerProtocol[
        NullProtocol,
        RequestContextProtocol,
        RequestDataProtocol[dict[str, str]],
        OobResponseProtocol[ExerciseStatus],
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
            return mark_safe(html + schema.oob_html)

        return html


class StartExerciseMixin(
    AbstractStartAction[OobResponseProtocol[ExerciseStatus]],
):
    """Execute start exercise handler's action."""

    def _start(self, **kwargs: object) -> OobResponseProtocol[ExerciseStatus]:
        return self.handler.execute(  # type: ignore
            params=NullDTO(),
            context=RequestContext(user=self.user),  # type: ignore
            data=RequestData(data={'action': ExerciseAction.CREATE_TASK}),
        )


class ProcessExerciseMixin(
    AbstractProcessAction[OobResponseProtocol[ExerciseStatus]],
):
    """Execute process exercise handler's action."""

    request: HttpRequest

    def _process(
        self, **kwargs: object
    ) -> OobResponseProtocol[ExerciseStatus]:
        return self.handler.execute(  # type: ignore
            params=NullDTO(),
            context=RequestContext(user=self.user),  # type: ignore
            data=RequestData(data=self.request.POST.dict()),
        )


class ExerciseLoopMixin(StartExerciseMixin, ProcessExerciseMixin):
    """Loop exercise handler."""
