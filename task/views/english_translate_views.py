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

from config.constants import PROGRES_MAX, PROGRES_MIN
from contrib.mixins_views import (
    CheckLoginPermissionMixin,
)
from english.analytics.english_analytics import collect_statistics
from english.models import WordModel, WordUserKnowledgeRelation
from task.forms import EnglishTranslateChoiceForm
from task.tasks import EnglishTranslateExercise


class EnglishTranslateChoiceView(CheckLoginPermissionMixin, TemplateView):
    """English exercise conditions choice view.

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
               'knowledge_assessment': ['S'],
               'timeout': 5,
               'user_id': 1,
           }
    """

    template_name = 'task/english/english_translate_choice.html'
    """The view template path (`str`).
    """

    def get_context_data(self, **kwargs: object) -> Dict[str, object]:
        """Add a form with a choice of exercise conditions.

        Adds :py:class:`~task.forms.english_translate_choice_form.EnglishTranslateChoiceForm`
        """  # noqa: E501, W505
        context = super().get_context_data()
        context['form'] = EnglishTranslateChoiceForm(request=self.request)
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        """Get user task condition.

        If the user task condition is valid, it is saved in the session
        and the user is redirected to learn the English word, returning
        an English word translation conditions selection form for the
        user to fill out, otherwise.
        """
        form = EnglishTranslateChoiceForm(request.POST, request=request)

        if form.is_valid():
            task_conditions = form.clean()
            task_conditions['user_id'] = request.user.id
            request.session['task_conditions'] = task_conditions
            return redirect(reverse_lazy('task:english_translate_demo'))

        context = {'form': EnglishTranslateChoiceForm(request=self.request)}
        return render(request, self.template_name, context)


class EnglishTranslateExerciseView(CheckLoginPermissionMixin, View):
    """English word translate exercise view."""

    template_name = 'task/english/english_translate_demo.html'
    """The view template path (`str`).
    """
    msg_key_error = 'Не все условия упражнения заданы'
    """Error message in condition ('str').
    """
    msg_no_words = 'По заданным условиям слов не найдено'
    """Message no words found (`str`).
    """
    redirect_no_words = {
        'redirect_no_words': reverse_lazy('task:english_translate_choice'),
    }

    def get(self, request: HttpRequest) -> HttpResponse:
        """Display an exercise page to translate a word."""
        task_conditions = request.session['task_conditions']
        task = EnglishTranslateExercise(**task_conditions)

        try:
            task.create_task()
        except KeyError:
            messages.error(request, self.msg_key_error)
            return redirect(reverse_lazy('task:english_translate_choice'))
        except ValueError:
            messages.error(request, self.msg_no_words)
            return redirect(reverse_lazy('task:english_translate_choice'))
        else:
            return render(request, self.template_name)

    def post(self, request: HttpRequest) -> JsonResponse:
        """Render the task."""
        task_conditions = request.session['task_conditions']
        task = EnglishTranslateExercise(**task_conditions)

        try:
            task.create_task()
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
                    **task.task_data,
                },
                status=200,
            )


@require_POST
@login_required
def update_words_knowledge_assessment_view(
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
    assessment = request.POST['assessment']
    word_pk = kwargs['word_id']

    try:
        word = WordModel.objects.get(pk=word_pk)
    except WordModel.DoesNotExist:
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    else:
        # Only owner have access to his word.
        if user != word.user:
            return HttpResponse(status=HTTPStatus.FORBIDDEN)

    obj, _ = WordUserKnowledgeRelation.objects.get_or_create(
        word=word, user=user
    )
    if assessment in {'+1', '-1'}:
        updated_assessment = obj.knowledge_assessment + int(assessment)
        if PROGRES_MIN <= updated_assessment <= PROGRES_MAX:
            obj.knowledge_assessment = updated_assessment
            obj.save(update_fields=['knowledge_assessment'])

    return JsonResponse({}, status=HTTPStatus.CREATED)
