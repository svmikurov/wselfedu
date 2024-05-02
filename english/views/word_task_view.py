from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from english.forms import WordChoiceHelperForm
from english.services import create_lookup_params

from english.services.word_favorites import (
    is_word_in_favorites,
    update_word_favorites_status,
)
from english.services.word_knowledge_assessment import (
    update_word_knowledge_assessment, get_knowledge_assessment,
)
from english.tasks.study_words import create_task

TITLE = {'title_name': 'Изучаем слова', 'url_name': 'english:word_choice'}
"""Заголовок страниц упражнения Изучаем слова (`dict`)

Содержит имя заголовка и ссылку на страницу выбора слов для упражнения.
Отображается посредством включения из templates/components/title.html.
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


class WordChoiceView(TemplateView):
    # Add only owner user
    """View choice English words to study."""

    template_name = 'english/tasks/word_choice.html'
    user_id = AnonymousUser.id
    extra_context = {
        'title': TITLE,
    }

    def get_context_data(self, **kwargs):
        """Add a user-specific words form to context."""
        self.user_id = self.request.user.id
        context = super().get_context_data(**kwargs)
        context['form'] = WordChoiceHelperForm(user_id=self.user_id)
        return context

    def post(self, request, *args, **kwargs):
        """Сохрани параметры фильтра слов для упражнения.

        Выполнит редирект на формирование задания и отображение вопроса.
        """
        user_id = request.user.id
        form = WordChoiceHelperForm(request.POST, user_id=user_id)

        if form.is_valid():
            form_data = form.cleaned_data
            lookup_params = create_lookup_params(form_data, user_id)
            language_order = form_data['language_order']

            request.session['lookup_params'] = lookup_params
            request.session['language_order'] = language_order

            return redirect(reverse_lazy('english:word_study_ajax'))
        else:
            return redirect(reverse_lazy('english:word_choice'))


class WordStudyView(View):
    """Представление для формирования задания и отображения вопроса."""

    template_name = 'english/tasks/word_study.html'

    def get(self, request, *args, **kwargs):
        """Создай задание и отобрази вопрос пользователю.
        """
        task = create_task(request)
        user_id = request.user.id
        word_id = task.get('word_id')
        knowledge = get_knowledge_assessment(word_id, user_id)
        favorites_status = is_word_in_favorites(user_id, word_id)

        context = {
            'title': TITLE,
            'task': task,
            'knowledge_assessment': knowledge,
            'favorites_status': favorites_status,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Get new word task."""
        task = create_task(request)
        user_id = request.user.id
        word_id = task.get('word_id')
        knowledge = get_knowledge_assessment(word_id, user_id)
        favorites_status = is_word_in_favorites(user_id, word_id)

        return JsonResponse(
            data={
                'task': task,
                'knowledge_assessment': knowledge,
                'favorites_status': favorites_status,
            },
            status=200,
        )


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

    return redirect(reverse_lazy('english:word_study_ajax'))


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
