"""
Solution for repetition and learning of words.
Before the solution, you need to select a category and source of words.
First, the question word is displayed, then the translation is added to it.
Words are displayed in random order.
The language of the question word is also displayed in random order.
A timeout is set between displays.
The solution continues until it is interrupted.
"""

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from config.settings import ANSWER_TIMEOUT, QUESTION_TIMEOUT
from english.models import CategoryModel, SourceModel

MESSAGE_NO_WORDS = 'Ничего не найдено, попробуйте другие варианты'


class ChooseEnglishWordsStudyView(TemplateView):
    """View choosing English words to study."""

    template_name = 'english/tasks/words_choose.html'
    categories = CategoryModel.objects.all()
    sources = SourceModel.objects.all()
    extra_context = {
        'categories': categories,
        'sources': sources,
        'message_no_words': MESSAGE_NO_WORDS,
    }


def study_english_words_view(request, **kwargs):
    """View to study English words.

    Parameters:
    -----------
    task_status: `str`
        ...

    """
    template_name = 'english/tasks/words_study.html'
    task_status = request.GET.get('task_status')

    if task_status == 'answer':
        # Отправь ответ пользователю.
        # Получи задание из сессии.
        task = request.session['task']
        context = {
            'task': task,
            'timeout': ANSWER_TIMEOUT
        }
        return render(request, template_name, context)

    # Отправь вопрос пользователю.
    try:
        task = ...
    except IndexError:
        # Не осталось слов, которые соответствуют фильтрам.
        messages.error(request, MESSAGE_NO_WORDS)
        return redirect(reverse_lazy('english:words_choose'))
    else:
        # Сохрани задание в сессию.
        request.session['task'] = task
        context = {
            'task': task,
            'timeout': QUESTION_TIMEOUT,
        }
        return render(request, template_name, context)
