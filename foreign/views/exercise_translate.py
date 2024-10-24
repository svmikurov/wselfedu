"""Views for word study task module."""

from http import HTTPStatus
from typing import Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from config.constants import (
    ASSESSMENT,
    FORM,
    PROGRESS,
    PROGRESS_MAX,
    PROGRESS_MIN,
    TASK_CONDITIONS,
    USER_ID,
    WORD_ID,
)
from contrib.views import (
    CheckLoginPermissionMixin,
)
from foreign.analytics.analytics import collect_statistics
from foreign.exercise.translate import TranslateExercise
from foreign.forms.word_choice import ForeignTranslateChoiceForm
from foreign.models import Word, WordProgress
from foreign.queries import update_word_favorites_status


class ForeignWordTranslateChoiceView(CheckLoginPermissionMixin, TemplateView):
    """Foreign word translate exercise conditions choice view.

    .. note::
        Task conditions may be:

        .. code-block:: python

           task_conditions = {
               'favorites': True,
               'language_order': 'RN',
               'category': 0,
               'source': 0,
               'period_start_date': 'NC',
               'period_end_date': 'DT',
               'word_count': ['OW', 'CB'],
               'progress': ['S'],
               'timeout': 5,
               'user_id': 1,
           }
    """

    template_name = 'foreign/exercise/foreign_translate_choice.html'
    """The view template path (`str`).
    """

    def get_context_data(self, **kwargs: object) -> Dict[str, object]:
        """Add a form with a choice of exercise conditions.

        Adds :py:class:`~foreign.forms.foreign_translate_choice_form.ForeignTranslateChoiceForm`
        """  # noqa: E501, W505
        context = super().get_context_data()
        context[FORM] = ForeignTranslateChoiceForm(request=self.request)
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        """Get user task condition.

        If the user task condition is valid, it is saved in the session
        and the user is redirected to learn the foreign word, returning
        a foreign word translation conditions selection form for the
        user to fill out, otherwise.
        """
        form = ForeignTranslateChoiceForm(request.POST, request=request)

        if form.is_valid():
            task_conditions = form.clean()
            task_conditions[USER_ID] = request.user.id
            request.session[TASK_CONDITIONS] = task_conditions
            return redirect(reverse_lazy('foreign:foreign_translate_demo'))

        context = {FORM: ForeignTranslateChoiceForm(request=self.request)}
        return render(request, self.template_name, context)


class ForeignTranslateExerciseView(CheckLoginPermissionMixin, View):
    """Foreign word translate exercise view."""

    template_name = 'foreign/exercise/foreign_translate_demo.html'
    """The view template path (`str`).
    """
    msg_key_error = 'Не все условия упражнения заданы'
    """Error message in condition ('str').
    """
    msg_no_words = 'По заданным условиям слов не найдено'
    """Message no words found (`str`).
    """
    redirect_no_words = {
        'redirect_no_words': reverse_lazy('foreign:foreign_translate_choice'),
    }

    def get(self, request: HttpRequest) -> HttpResponse:
        """Display an exercise page to translate a word."""
        task_conditions = request.session[TASK_CONDITIONS]
        task = TranslateExercise(task_conditions)

        try:
            task.create_task()
        except KeyError:
            messages.error(request, self.msg_key_error)
            return redirect(reverse_lazy('foreign:foreign_translate_choice'))
        except (ValueError, IndexError):
            messages.error(request, self.msg_no_words)
            return redirect(reverse_lazy('foreign:foreign_translate_choice'))
        else:
            return render(request, self.template_name)

    def post(self, request: HttpRequest) -> JsonResponse:
        """Render the task."""
        task_conditions = request.session[TASK_CONDITIONS]
        task = TranslateExercise(task_conditions)

        try:
            task_data = task.task_data
        except ValueError:
            messages.error(request, self.msg_no_words)
            return JsonResponse(
                data=self.redirect_no_words,
                status=412,
            )
        else:
            collect_statistics(task=task)
            return JsonResponse(
                data={
                    **self.redirect_no_words,
                    **task_data,
                },
                status=200,
            )


@require_POST
@login_required
def update_word_progress_view(
    request: HttpRequest,
    **kwargs: object,
) -> JsonResponse | HttpResponse:
    """Update user word knowledge assessment view.

    :param HttpRequest request: Request to update user word knowledge
     assessment.
    :param object kwargs: ID of the word whose progress will be updated.

     ``kwargs`` fields:
       - ``'word_id'``: word ID (`int`).

    :return: Response without data, with status 201.
    :rtype: JsonResponse
    """
    user = request.user
    assessment = request.POST.get(ASSESSMENT)
    word_pk = kwargs[WORD_ID]

    try:
        word = Word.objects.get(pk=word_pk)
    except Word.DoesNotExist:
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    else:
        # Only owner have access to his word.
        if user != word.user:
            return HttpResponse(status=HTTPStatus.FORBIDDEN)

    obj, _ = WordProgress.objects.get_or_create(word=word, user=user)

    if assessment in {'+1', '-1'}:
        updated_progress = obj.progress + int(assessment)
        if PROGRESS_MIN <= updated_progress <= PROGRESS_MAX:
            obj.progress = updated_progress
            obj.save(update_fields=[PROGRESS])

    return JsonResponse({}, status=HTTPStatus.CREATED)


@require_POST
@login_required
def update_words_favorites_status_view_ajax(
    request: HttpRequest,
    **kwargs: Dict[str, object],
) -> JsonResponse:
    """Update the status of a word, is it favorite.

    This view receives a request from Ajax when the user wants to
    update the status of a word.

    Parameters
    ----------
    request : `HttpRequest`
        Http request.
    kwargs : `Dict[str, object]`
        The keyword argument that contains the ``word_id`` of the word
        whose status should be updated.

    Return
    ------
    response : `JsonResponse`
        Response with current favorite word status.

    """
    word_id = kwargs[WORD_ID]
    user_id = request.user.pk
    favorites_status = update_word_favorites_status(word_id, user_id)

    # this view gets a request from Ajax
    response = JsonResponse(
        data={
            'favorites_status': favorites_status,
        },
        status=201,
    )
    return response
