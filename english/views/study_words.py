#
# Данный модуль является часть приложения по изучению английского языка.
#
"""Представления пользователю для изучения, повторения, проверки знания слов.
"""

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from config.settings import ANSWER_TIMEOUT, QUESTION_TIMEOUT
from english.models import CategoryModel, SourceModel
from english.services.serve_query import all_objects
from english.tasks.study_words import create_task_study_words

MESSAGE_NO_WORDS = 'Ничего не найдено, попробуйте другие варианты'
"""Нет слов, удовлетворяющих критериям выборки пользователя (`str`)
"""


class ChooseEnglishWordsStudyView(TemplateView):
    """View choosing English words to study."""

    template_name = 'english/tasks/words_choose.html'
    categories = all_objects(CategoryModel.objects)
    sources = all_objects(SourceModel.objects)
    extra_context = {
        'categories': categories,
        'sources': sources,
        'message_no_words': MESSAGE_NO_WORDS,
        'task_status': 'start',
        'next_url': 'english:words_choose',
    }


def study_english_words_view(request, **kwargs):
    """View to study English words.
    """
    template_name = 'english/tasks/words_study.html'
    task_status = request.GET.get('task_status')

    if task_status == 'answer':
        # Отправь ответ пользователю.
        # Получи задание из сессии.
        task = request.session['task']
        context = {
            'task': task,
            'timeout': ANSWER_TIMEOUT,
            'next_url': 'english:words_study',
        }
        return render(request, template_name, context)

    # Отправь вопрос пользователю.
    try:
        task = create_task_study_words(request)
    except ValueError:
        # Не осталось слов, которые соответствуют фильтрам.
        messages.error(request, MESSAGE_NO_WORDS)
        return redirect(reverse_lazy('english:words_choose'))
    else:
        # Сохрани задание в сессию.
        request.session['task'] = task
        context = {
            'task': task,
            'timeout': QUESTION_TIMEOUT,
            'next_url': 'english:words_study',
        }
        return render(request, template_name, context)
