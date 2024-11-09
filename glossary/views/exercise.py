"""Views for term study.

.. todo::
   * develop the collect_statistics at TermExerciseView.
"""

from http import HTTPStatus

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from rest_framework import status

from config.constants import MSG_NO_TASK, PROGRESS_MAX, PROGRESS_MIN
from contrib.views import (
    CheckLoginPermissionMixin,
)
from glossary.exercise.question import GlossaryExercise
from glossary.forms.term_choice import GlossaryParamsForm
from glossary.models import Glossary
from glossary.queries.exercise import save_params


class GlossaryParamsView(CheckLoginPermissionMixin, TemplateView):
    """Glossary term exercise conditions choice view."""

    template_name = 'glossary/exercise/params.html'
    """The view template path (`str`).
    """

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Add exercise params form to context."""
        context = super().get_context_data()
        context['form'] = GlossaryParamsForm(request=self.request)
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        """Get user task condition."""
        form = GlossaryParamsForm(request.POST, request=request)
        user = request.user

        if form.is_valid():
            task_conditions = form.clean()

            if task_conditions.pop('save_params'):
                save_params(user, task_conditions)

            task_conditions['user_id'] = user.id
            request.session['task_conditions'] = task_conditions
            return redirect(reverse_lazy('glossary:exercise'))

        context = {'form': GlossaryParamsForm(request=self.request)}
        return render(request, self.template_name, context)


class TermExerciseView(CheckLoginPermissionMixin, View):
    """Glossary term study exercise view."""

    template_name = 'glossary/exercise/exercise.html'
    """The view template path (`str`).
    """
    msg_key_error = 'Не все условия упражнения заданы'
    """Error message in condition ('str').
    """
    msg_no_terms = MSG_NO_TASK
    """Message no terms found (`str`).
    """
    redirect_no_terms = {
        'redirect_no_terms': reverse_lazy('glossary:params'),
    }

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render the page template for exercise."""
        task_conditions = request.session['task_conditions']
        task = GlossaryExercise(task_conditions)

        try:
            task.create_task()
        except KeyError:
            messages.error(request, self.msg_key_error)
            return redirect(reverse_lazy('glossary:params'))
        except (ValueError, IndexError):
            messages.error(request, self.msg_no_terms)
            return redirect(reverse_lazy('glossary:params'))
        else:
            return render(request, self.template_name)

    def post(self, request: HttpRequest) -> JsonResponse:
        """Render the task."""
        task_conditions = request.session['task_conditions']
        task = GlossaryExercise(task_conditions)

        try:
            task_data = task.task_data
        except ValueError:
            messages.error(request, self.msg_no_terms)
            return JsonResponse(
                data=self.redirect_no_terms,
                status=412,
            )
        else:
            # TODO: develop the collect_statistics  # noqa: TD003, TD002
            # collect_statistics(task=task)
            return JsonResponse(
                data={
                    **self.redirect_no_terms,
                    **task_data,
                },
                status=200,
            )


@require_POST
@login_required
def update_term_favorite_status_view_ajax(
    request: HttpRequest,
    **kwargs: dict[str, object],
) -> JsonResponse:
    """Update the status of a term, is it favorite."""
    term_id = kwargs['term_id']
    term = Glossary.objects.get(pk=term_id, user=request.user)
    term.favorites = not term.favorites
    term.save()

    # this view gets a request from Ajax
    response = JsonResponse(
        data={
            'favorites_status': term.favorites,
        },
        status=201,
    )
    return response


@require_POST
@login_required
def update_term_study_progress(
    request: HttpRequest,
    **kwargs: object,
) -> HttpResponse:
    """Update term study progres."""
    user = request.user
    assessment = request.POST.get('assessment')
    term_pk = kwargs['term_id']

    try:
        obj = Glossary.objects.get(pk=term_pk)
    except Glossary.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    else:
        # Only owner have access to his term.
        if user != obj.user:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

    if assessment in {'+1', '-1'}:
        updated_progress = obj.progress + int(assessment)
        if PROGRESS_MIN <= updated_progress <= PROGRESS_MAX:
            obj.progress = updated_progress
            obj.save(update_fields=['progress'])

    return JsonResponse({}, status=HTTPStatus.CREATED)
