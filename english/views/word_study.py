#
# Данный модуль является частью приложения по изучению английского языка.
#

"""
Модуль содержит представления для изучения, повторения, проверки знания
перевода слов.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView

from english.models import (
    CategoryModel,
    SourceModel,
)
from english.services.serve_request import (
    get_lookup_parameters,
    set_lookup_parameters,
)
from english.services.words_favorites import (
    is_word_in_favorites,
    update_words_favorites_status,
)
from english.services.words_knowledge_assessment import (
    get_knowledge_assessment,
    update_word_knowledge_assessment,
)
from english.tasks.study_words import create_task_study_words


TITLE = {'title_name': 'Изучаем слова', 'url_name': 'english:words_choose'}
"""Заголовок страниц упражнения Изучаем слова (`dict`)

Содержит имя заголовка и ссылку на страницу выбора слов для упражнения.
Отображается посредством включения из templates/components/card_title.html.
"""
QUESTION_TIMEOUT = 5000
"""Время на отображения вопроса на странице пользователя (`int`).
"""
ANSWER_TIMEOUT = 5000
"""Время на отображения ответа на странице пользователя (`int`).
"""
MSG_NO_WORDS = 'Ничего не найдено, попробуйте другие варианты'
"""Нет слов, удовлетворяющих критериям выборки пользователя (`str`).
"""
RESTART_MSG = 'Выберите условия задания'
"""Сообщение о необходимости заново установить параметры выбора слова, в случае
ошибки приложения (`str`).
"""


class ChooseEnglishWordsStudyView(TemplateView):
    """View choosing English words to study."""

    template_name = 'english/tasks/words_choose.html'
    categories = CategoryModel.objects.all()
    sources = SourceModel.objects.all()

    extra_context = {
        'title': TITLE,
        'categories': categories,
        'sources': sources,
        'message_no_words': MSG_NO_WORDS,
        'next_url': 'english:words_choose',
    }


@require_GET
def start_study_word_view(request, *args, **kwargs):
    """Установи параметры выборки слов для упражнения.

    Выполнит редирект на формирование и отображение вопроса из упражнения.
    """
    set_lookup_parameters(request)
    return redirect(reverse_lazy('english:word_study_question'))


class QuestionWordStudyView(View):
    """Представление для формирования задания и отображения вопроса."""

    template_name = 'english/tasks/word_study.html'
    params_choice_url = reverse_lazy('english:words_choose')

    def get(self, request, *args, **kwargs):
        """Создай задание и отобрази вопрос пользователю.
        """
        user_id = request.user.id

        try:
            lookup_params = get_lookup_parameters(request)
        except AttributeError:
            messages.error(request, RESTART_MSG)
            return redirect(self.params_choice_url)
        else:
            task = create_task_study_words(lookup_params, user_id)

        if not task:
            messages.error(request, MSG_NO_WORDS)
            return redirect(self.params_choice_url)
        else:
            request.session['task'] = task

        word_id = task.get('word_id')
        knowledge = get_knowledge_assessment(word_id, user_id)
        favorites_status = is_word_in_favorites(user_id, word_id)

        context = {
            'title': TITLE,
            'task': task,
            'timeout': QUESTION_TIMEOUT,
            'next_url': 'english:word_study_answer',
            'task_status': 'question',
            'knowledge_assessment': knowledge,
            'favorites_status': favorites_status,
        }

        return render(request, self.template_name, context)


class AnswerWordStudyView(View):
    """Представление для отображения ответа."""

    template_name = 'english/tasks/word_study.html'
    params_choice_url = reverse_lazy('english:words_choose')

    def get(self, request, *args, **kwargs):
        """Покажи пользователю перевод слова.
        """
        user_id = request.user.id

        try:
            task = request.session['task']
        except ValueError:
            messages.error(request, RESTART_MSG)
            return redirect(self.params_choice_url)

        word_id = task.get('word_id')
        knowledge = get_knowledge_assessment(word_id, user_id)
        favorites_status = is_word_in_favorites(user_id, word_id)

        context = {
            'title': TITLE,
            'task': task,
            'timeout': ANSWER_TIMEOUT,
            'next_url': 'english:word_study_question',
            'task_status': 'answer',
            'knowledge_assessment': knowledge,
            'favorites_status': favorites_status,
        }

        return render(request, self.template_name, context)


@require_POST
@login_required
def update_words_knowledge_assessment_view(request, **kwargs):
    """Изменяет в модели WordUserKnowledgeRelation значение поля
       knowledge_assessment (самооценки пользователем знания слова),
       если, во время выполнения пользователем задания, изменении самооценки
       и оставит ее значение в установленных пределах.
       Минимальное значение самооценки равно MIN_KNOWLEDGE_ASSESSMENT,
       максимальное равно MAX_KNOWLEDGE_ASSESSMENT.
    """
    given_assessment = int(request.POST['knowledge_assessment'])
    word_pk = kwargs['word_id']
    user_pk = request.user.pk

    if given_assessment:
        old_assessment = get_knowledge_assessment(word_pk, user_pk)
        new_assessment = old_assessment + given_assessment
        update_word_knowledge_assessment(word_pk, user_pk, new_assessment)

    return redirect(reverse_lazy('english:word_study_question'))


@require_POST
@login_required
def update_words_favorites_status_view(request, **kwargs):
    """Обнови статус слова, избранное ли оно.

    После обновления совершит редирект на формирование нового задания.
    """
    favorites_action = request.POST.get('favorites_action')
    word_id = kwargs['word_id']
    user_id = request.user.pk

    update_words_favorites_status(word_id, user_id, favorites_action)
    # Редирект на формирование нового задания.
    return redirect(reverse_lazy('english:word_study_question'))
