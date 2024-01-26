# Нужен рефакторинг!
# Вынести из представлений работу с БД.
# Упростить логику.

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

from config import settings
from english.models import (
    CategoryModel,
    SourceModel,
    WordModel,
)
from english.services import (
    is_word_in_favorites,
    get_or_create_knowledge_assessment
)
from english.tasks.repetition_task import (
    choice_word,
    add_filers_to_queryset,
)

TITLE = {'title_name': 'Изучаем слова', 'url_name': 'eng:start_repetition'}
QUESTION_TIMEOUT = settings.QUESTION_TIMEOUT
ANSWER_TIMEOUT = settings.ANSWER_TIMEOUT
BTN_NAME = 'Начать'


class StartRepetitionWordsView(TemplateView):
    """Start solution.

    In this View is selected the category and source of repeated words.
    After this solution is redirected
    to another View in which it alternates words
    """
    categories = CategoryModel.objects.all()
    sources = SourceModel.objects.all()
    template_name = 'eng/tasks/start_repetition.html'

    extra_context = {
        'title': TITLE,
        'categories': categories,
        'sources': sources,
        'task_status': 'start',
        'btn_name': BTN_NAME,
        'next_url': 'eng:repetition',
    }


class RepetitionWordsView(View):
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        task_status: str = kwargs.get('task_status')

        # Получаем QuerySet всех слов.
        words_qs = WordModel.objects.all()
        # Применяем фильтрацию к QuerySet, если имеются фильтры.
        filtered_words: list[dict] = add_filers_to_queryset(
            request, words_qs, task_status,
        )

        # Запускаем задание.
        if task_status == 'question' or task_status == 'start':
            try:
                # Получи слово для задания.
                task = choice_word(filtered_words)
            except IndexError:
                messages.error(
                    self.request,
                    'Ничего не найдено, попробуйте другие варианты'
                )
                return redirect(reverse_lazy('eng:start_repetition'))
            else:
                # Сохрани задание в сессию, если статус - вопрос.
                request.session['task'] = task
                timeout = QUESTION_TIMEOUT
        else:
            # Получи задание из сессии, если статус - ответ.
            task = request.session['task']
            timeout = ANSWER_TIMEOUT

        # Формируем context.
        word_id = task.get('word_id', '')
        words_eng = WordModel.objects.get(pk=word_id)
        favorites_status: bool = is_word_in_favorites(user_id, word_id)

        context = {
            'title': TITLE,
            'task_status': task_status,
            'task': task,
            'timeout': timeout,
            'next_url': 'eng:repetition',
            'word_id': word_id,
            'words_eng': words_eng,
            'favorites_status': favorites_status,
        }
        # Получаем или добавляем в БД значение самооценки пользователя уровня
        # знания слова.
        # Добавляем в context значение самооценки пользователя уровня знания
        # слова.
        if request.user.is_authenticated:
            context[
                'knowledge_assessment'
            ] = get_or_create_knowledge_assessment(word_id, user_id)
        # Отправляем задание пользователю.
        return render(request, 'eng/tasks/repetition.html', context)
