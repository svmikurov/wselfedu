from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from contrib_app.mixins import (
    CheckLoginPermissionMixin,
)
from english.services import (
    get_knowledge_assessment,
    update_word_knowledge_assessment,
    update_word_favorites_status,
)
from task.forms import EnglishTranslateChoiceForm
from task.tasks import EnglishTranslateExercise


class EnglishTranslateChoiceView(CheckLoginPermissionMixin, TemplateView):
    """English translate choice View.

    Notes:
    -----
    Task conditions may be:
        ``task_conditions`` = {
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
    TITLE = 'Выберите условия задания'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.TITLE
        context['form'] = EnglishTranslateChoiceForm(request=self.request)
        return context

    def post(self, request):
        form = EnglishTranslateChoiceForm(request.POST, request=request)

        if form.is_valid():
            task_conditions = form.clean()
            task_conditions['user_id'] = request.user.id
            request.session['task_conditions'] = task_conditions

            return redirect(reverse_lazy('task:english_translate_demo'))

        context = {
            'title': self.TITLE,
            'form': EnglishTranslateChoiceForm(request=self.request),
        }
        return render(request, self.template_name, context)


class EnglishTranslateExerciseView(CheckLoginPermissionMixin, View):
    """English word translate exercise view."""

    template_name = 'task/english/english_translate_demo.html'
    msg_key_error = 'Не задан таймаут или порядок перевода слов'
    msg_no_words = 'По заданным условиям слов не найдено'
    redirect_no_words = reverse_lazy('task:english_translate_choice')

    def get(self, request, *args, **kwargs):
        """Display an exercise page to translate an English word."""
        try:
            task_conditions = request.session['task_conditions']
            task = EnglishTranslateExercise(**task_conditions)
        except KeyError:
            messages.error(request, self.msg_key_error)
            return redirect(self.redirect_no_words)

        task.create_task()
        if task.word_count == 0:
            messages.error(request, self.msg_no_words)
            return redirect(self.redirect_no_words)

        # If the task is created, display the task page
        context = {
            'title': {
                'title_name': 'Изучаем слова',
                'url_name': 'task:english_translate_choice',
            },
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Get new word for English word translate exercise page."""
        task_conditions = request.session['task_conditions']
        task = EnglishTranslateExercise(**task_conditions)
        task.create_task()

        if task.word_count > 0:
            return JsonResponse(
                data={
                    'redirect_no_words': self.redirect_no_words,
                    'question_text': task.question_text,
                    'answer_text': task.answer_text,
                    'timeout': task.timeout,
                    'word_count': task.word_count,
                    'knowledge': task.knowledge,
                    'knowledge_url': task.knowledge_url,
                    'favorites_status': task.favorites_status,
                    'favorites_url': task.favorites_url,
                    'google_translate_word_link': task.google_translate_word_link,
                },
            )
        else:
            messages.error(request, self.msg_no_words)
            return JsonResponse(
                data={
                    'redirect_no_words': self.redirect_no_words,
                },
                status=412,
            )


@require_POST
@login_required
def update_words_knowledge_assessment_view(request, **kwargs):
    """"""
    assessment = request.POST['assessment']
    word_pk = kwargs['word_id']
    user_pk = request.user.pk

    if assessment in {'+1', '-1'}:
        old_assessment = get_knowledge_assessment(word_pk, user_pk)
        new_assessment = old_assessment + int(assessment)
        update_word_knowledge_assessment(word_pk, user_pk, new_assessment)

    return JsonResponse({}, status=201)


@require_POST
@login_required
def update_words_favorites_status_view_ajax(request, **kwargs):
    """Обнови статус слова, избранное ли оно."""
    word_id = kwargs['word_id']
    user_id = request.user.pk
    favorites_status = update_word_favorites_status(word_id, user_id)

    return JsonResponse(
        data={
            'favorites_status': favorites_status,
        },
        status=201,
    )
