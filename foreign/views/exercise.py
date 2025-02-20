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

from config.constants import (
    MSG_NO_TASK,
    PROGRESS_MAX,
    PROGRESS_MIN,
)
from contrib.views.exercise import ExerciseParamsView
from contrib.views.general import (
    CheckLoginPermissionMixin,
)
from foreign.analytics.analytics import collect_statistics
from foreign.exercise.translate import TranslateExercise
from foreign.forms.word_choice import ForeignTranslateChoiceForm
from foreign.models import (
    Word,
    WordProgress,
)
from foreign.queries import update_word_favorites_status
from foreign.queries.exercise import save_params


class ForeignExerciseParamsView(ExerciseParamsView):
    """Foreign word exercise conditions choice view."""

    template_name = 'foreign/exercise/foreign_translate_choice.html'
    exercise_url = reverse_lazy('foreign:foreign_translate_demo')
    form = ForeignTranslateChoiceForm

    def save_params(self, *args: object, **kwargs: object) -> None:
        """Save exercise params."""
        save_params(*args, **kwargs)


class WordExerciseView(CheckLoginPermissionMixin, View):
    """Foreign word translate exercise view."""

    template_name = 'foreign/exercise/foreign_translate_demo.html'
    """The view template path (`str`).
    """
    msg_key_error = 'Не все условия упражнения заданы'
    """Error message in condition ('str').
    """
    msg_no_words = MSG_NO_TASK
    """Message no words found (`str`).
    """
    redirect_no_words = {
        'redirect_no_words': reverse_lazy('foreign:params'),
    }

    def get(self, request: HttpRequest) -> HttpResponse:
        """Display an exercise page to translate a word."""
        task_conditions = request.session['task_conditions']
        task = TranslateExercise(task_conditions)

        try:
            task.create_task()
        except KeyError:
            messages.error(request, self.msg_key_error)
            return redirect(reverse_lazy('foreign:params'))
        except (ValueError, IndexError):
            messages.error(request, self.msg_no_words)
            return redirect(reverse_lazy('foreign:params'))
        else:
            return render(request, self.template_name)

    def post(self, request: HttpRequest) -> JsonResponse:
        """Render the task."""
        task_conditions = request.session['task_conditions']
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
    assessment = request.POST.get('assessment')
    word_pk = kwargs['word_id']

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
            obj.save(update_fields=['progress'])

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
    word_id = kwargs['word_id']
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
