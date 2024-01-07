"""
Solution for repetition and learning of words.
Before the solution, you need to select a category and source of words.
First, the question word is displayed, then the translation is added to it.
Words are displayed in random order.
The language of the question word is also displayed in random order.
A timeout is set between displays.
The solution continues until it is interrupted.
"""
import logging

from django.contrib import messages
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from english.models import (
    CategoryModel,
    SourceModel,
    WordModel,
    WordUserKnowledgeRelation,
)
from english.tasks.repetition_task import (
    choice_word,
    add_filers_to_queryset,
)
from english.models.words import get_knowledge_assessment
from users.models import UserModel

TITLE = 'Изучаем слова'
QUESTION_TIMEOUT = 3000  # ms
ANSWER_TIMEOUT = 3000  # ms
BTN_NAME = 'Начать'

INDEX_ERROR_MESSAGE = 'Ничего не найдено, попробуйте другие варианты'

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    filename='myapp.log',
    level=logging.DEBUG,
)


class StartRepetitionWordsView(TemplateView):
    """Start solution.

    In this View is selected the category and source of repeated words.
    After this solution is redirected
    to another View in which it alternates words
    """
    categories = CategoryModel.objects.all()
    sources = SourceModel.objects.all()

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
                messages.error(self.request, INDEX_ERROR_MESSAGE)
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
        context = {
            'title': TITLE,
            'task_status': task_status,
            'task': task,
            'timeout': timeout,
            'next_url': 'eng:repetition',
            'word_id': word_id,
        }
        # Получаем или добавляем в БД значение самооценки пользователя уровня
        # знания слова.
        # Добавляем в context значение самооценки пользователя уровня знания
        # слова.
        if request.user.is_authenticated:
            context[
                'knowledge_assessment'
            ] = get_knowledge_assessment(word_id, user_id)

        # Отправляем задание пользователю.
        return render(request, 'eng/tasks/repetition.html', context)


def knowledge_assessment_view(request, *args, **kwargs):
    """Изменяет в модели WordUserKnowledgeRelation значение поля
    knowledge_assessment (самооценки пользователем знания слова).
    """
    # Если пользователь аутентифицирован, обнови его самооценку знания слова.
    if request.user.is_authenticated:
        current_assessment = request.POST['knowledge_assessment']
        word_pk = kwargs['word_id']
        user_pk = request.user.pk

        # Обнови самооценку знания слова.
        WordUserKnowledgeRelation.objects.filter(
            word=WordModel.objects.get(pk=word_pk),
            user=UserModel.objects.get(pk=user_pk),
        ).update(
            knowledge_assessment=F('knowledge_assessment') + current_assessment
        )

    # Редирект на формирование нового задания.
    kwargs = {'task_status': 'question'}
    return redirect(reverse_lazy('eng:repetition', kwargs=kwargs))
