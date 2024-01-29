#
# Данный модуль является частью приложения по изучению английского языка.
#
"""Представления пользователю для изучения, повторения, проверки знания слов.
"""

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from english.models import CategoryModel, SourceModel
from english.services.serve_request import save_lookup_parameters_to_session
from english.tasks.study_words import create_task_study_words

QUESTION_TIMEOUT = 5000
ANSWER_TIMEOUT = 5000
"""Время на отображения вопроса и ответа задания на странице пользователя."""

MESSAGE_NO_WORDS = 'Ничего не найдено, попробуйте другие варианты'
"""Нет слов, удовлетворяющих критериям выборки пользователя (`str`)
"""


class ChooseEnglishWordsStudyView(TemplateView):
    """View choosing English words to study."""

    template_name = 'english/tasks/words_choose.html'
    categories = CategoryModel.objects.all()
    sources = SourceModel.objects.all()
    extra_context = {
        'categories': categories,
        'sources': sources,
        'message_no_words': MESSAGE_NO_WORDS,
        'task_status': 'start',
        'next_url': 'english:words_choose',
    }


class StudyWordsView(TemplateView):
    def get(self, request, *args, **kwargs):
        """View to study English words.
        """
        template_name = 'english/tasks/words_study.html'
        task_status = kwargs.get('task_status')

        # Покажи пользователю перевод слова.
        if task_status == 'answer':
            print('answer')
            task = request.session['task']
            context = {
                'task': task,
                'timeout': ANSWER_TIMEOUT,
                'next_url': 'english:words_study',
                'task_status': 'answer',
            }
            return render(request, template_name, context)

        # Покажи пользователю слово для перевода.
        if task_status == 'question' or task_status == 'start':
            if task_status == 'start':
                save_lookup_parameters_to_session(request)

            try:
                lookup_parameters = request.session['lookup_parameters']
                task = create_task_study_words(lookup_parameters)
            except ValueError:
                messages.error(request, MESSAGE_NO_WORDS)
                return redirect(reverse_lazy('english:words_choose'))
            else:
                request.session['task'] = task
                context = {
                    'task': task,
                    'timeout': QUESTION_TIMEOUT,
                    'next_url': 'english:words_study',
                    'task_status': 'question',
                }
                return render(request, template_name, context)

        # Редирект на страницу формирования параметров поиска слова.
        return redirect(reverse_lazy('english:words_choose'))
