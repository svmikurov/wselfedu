from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from english.services.words_knowledge_assessment import (
    get_word_knowledge_assessment,
    update_word_knowledge_assessment,
)
from english.services.words_favorites import update_words_favorites_status


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
    kwargs = {'task_status': 'question'}

    if given_assessment:
        old_assessment = get_word_knowledge_assessment(user_pk, word_pk)
        new_assessment = old_assessment + given_assessment
        update_word_knowledge_assessment(user_pk, word_pk, new_assessment)

    return redirect(reverse_lazy('english:words_study', kwargs=kwargs))


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
    kwargs = {'task_status': 'question'}
    return redirect(reverse_lazy('english:words_study', kwargs=kwargs))
