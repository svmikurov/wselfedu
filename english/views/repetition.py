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
from django.views import View
from django.views.generic import TemplateView

from english.models import (
    CategoryModel,
    SourceModel,
)
from english.tasks.repetition_task import create_task

TITLE = 'Переведи слова'
DEFAULT_CATEGORY = 'Все категории'
DEFAULT_CATEGORY_ID = 0
DEFAULT_SOURCE = 'Учебник'
DEFAULT_SOURCE_ID = 1
QUESTION_TIMEOUT = 8000     # ms
ANSWER_TIMEOUT = 8000       # ms
BTN_NAME = 'Начать'

INDEX_ERROR_MESSAGE = 'Ничего не найдено, попробуйте другие варианты'


class StartRepetitionWordsView(TemplateView):
    """
    Start solution.
    In this View is selected the category and source of repeated words.
    After this solution is redirected
    to another View in which it alternates words
    """
    categories = CategoryModel.objects.all()
    sources = SourceModel.objects.all()

    extra_context = {
        'title': TITLE,
        'categories': categories,
        'default_category': DEFAULT_CATEGORY,
        'default_category_id': DEFAULT_CATEGORY_ID,
        'sources': sources,
        'default_source': DEFAULT_SOURCE,
        'default_source_id': DEFAULT_SOURCE_ID,
        'task_status': 'question',
        'btn_name': BTN_NAME,
        'next_url': 'eng:repetition',
    }


class RepetitionWordsView(View):
    def get(self, request, *args, **kwargs):
        task_status: str = kwargs.get('task_status')
        selected_category = request.GET.get('selected_category')
        selected_source = request.GET.get('selected_source')

        if selected_category:
            request.session['selected_category'] = selected_category
            request.session['selected_source'] = selected_source
        else:
            selected_category = request.session['selected_category']
            selected_source = request.session['selected_source']

        if selected_category == 0:
            is_category_selected = False
        else:
            is_category_selected = True

        if task_status == 'question':
            try:
                task = create_task(
                    selected_category,
                    is_category_selected,
                    selected_source,
                )
            except IndexError:
                messages.error(self.request, INDEX_ERROR_MESSAGE)
                return redirect(reverse_lazy('eng:start_repetition'))
            else:
                request.session['task'] = task
                timeout = QUESTION_TIMEOUT
        else:
            task = request.session['task']
            timeout = ANSWER_TIMEOUT

        category_name = CategoryModel.objects.get(pk=selected_category).name
        source_name = SourceModel.objects.get(pk=selected_source).name

        context = {
            'title': TITLE,
            # 'category': category_name,    # temporarily not used
            # 'source': source_name,        # temporarily not used
            'task_status': task_status,
            'task': task,
            'timeout': timeout,
            'next_url': 'eng:repetition',
        }

        return render(request, 'eng/tasks/repetition.html', context)
