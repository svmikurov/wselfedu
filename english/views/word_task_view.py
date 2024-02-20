from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView

from english.forms import WordChoiceHelperForm

from english.services.serve_request import (
    get_lookup_params,
    save_lookup_params,
    set_lookup_params,
)
from english.services.word_favorites import (
    is_word_in_favorites,
    update_word_favorites_status,
)
from english.services.word_knowledge_assessment import (
    update_word_knowledge_assessment, get_knowledge_assessment,
)
from english.tasks.study_words import create_task_study_words

TITLE = {'title_name': 'Изучаем слова', 'url_name': 'english:word_choice'}
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
CHOICE_PATH = 'english:word_choice'
QUESTION_PATH = 'english:word_study_question'
ANSWER_PATH = 'english:word_study_answer'


class WordChoiceView(TemplateView):
    """View choice English words to study."""

    template_name = 'english/tasks/word_choice.html'
    url = reverse_lazy(CHOICE_PATH)
    redirect_url = reverse_lazy(QUESTION_PATH)

    form_choice = WordChoiceHelperForm()
    extra_context = {
        'title': TITLE,
        'form_choice': form_choice,
    }

    def post(self, request, *args, **kwargs):
        """Сохрани параметры фильтра слов для упражнения.

        Выполнит редирект на формирование задания и отображение вопроса.
        """
        lookup_params = set_lookup_params(request)
        if lookup_params:
            save_lookup_params(request, lookup_params)
            return redirect(self.redirect_url)
        else:
            return redirect(self.url)


@require_GET
def start_study_word_view(request, *args, **kwargs):
    """Установи параметры выборки слов для упражнения.

    Создаст параметры фильтрации для поиска.
    Сохранит параметры фильтрации.
    Выполнит редирект на формирование и отображение вопроса из упражнения.
    """
    redirect_url = reverse_lazy(QUESTION_PATH)

    lookup_params = set_lookup_params(request)
    if lookup_params:
        save_lookup_params(request, lookup_params)

    return redirect(redirect_url)


class QuestionWordStudyView(View):
    """Представление для формирования задания и отображения вопроса."""

    template_name = 'english/tasks/word_study.html'
    params_choice_url = reverse_lazy(CHOICE_PATH)

    def get(self, request, *args, **kwargs):
        """Создай задание и отобрази вопрос пользователю.
        """
        user_id = request.user.id

        try:
            lookup_params = get_lookup_params(request)
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
            'next_url': ANSWER_PATH,
            'task_status': 'question',
            'knowledge_assessment': knowledge,
            'favorites_status': favorites_status,
        }

        return render(request, self.template_name, context)


class AnswerWordStudyView(View):
    """Представление для отображения ответа."""

    template_name = 'english/tasks/word_study.html'
    params_choice_url = reverse_lazy(CHOICE_PATH)

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
            'next_url': QUESTION_PATH,
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
    action = request.POST['action']
    word_pk = kwargs['word_id']
    user_pk = request.user.pk

    if action in {'+1', '-1'}:
        old_assessment = get_knowledge_assessment(word_pk, user_pk)
        new_assessment = old_assessment + int(action)
        update_word_knowledge_assessment(word_pk, user_pk, new_assessment)
    elif action in {QUESTION_PATH, ANSWER_PATH}:
        return redirect(action)

    return redirect(reverse_lazy(QUESTION_PATH))


@require_POST
@login_required
def update_words_favorites_status_view(request, **kwargs):
    """Обнови статус слова, избранное ли оно.

    После обновления совершит редирект на формирование нового задания.
    """
    favorites_action = request.POST.get('favorites_action')
    word_id = kwargs['word_id']
    user_id = request.user.pk
    request_from_page = kwargs['from_page']
    redirect_url = 'english:home'

    update_word_favorites_status(word_id, user_id, favorites_action)

    if request_from_page == 'user_list':
        redirect_url = reverse_lazy(
            'english:users_words',
            kwargs={'pk': user_id},
        )
    elif request_from_page == 'word_study':
        # Редирект на формирование нового задания.
        redirect_url = reverse_lazy(QUESTION_PATH)

    return redirect(redirect_url)
