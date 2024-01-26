from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from english.services.words_knowledge_assessment import (
    get_word_knowledge_assessment,
    update_word_knowledge_assessment,
)
from english.services.words_favorites import (
    add_word_to_favorites,
    remove_word_from_favorites
)


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

    return redirect(reverse_lazy('eng:repetition', kwargs=kwargs))


@require_POST
@login_required
def update_words_favorites_status_view(request, **kwargs):
    """Если слова нет среди избранных - добавляет слово в избранные,
       если слово среди избранных - убирает слово из избранных.
    """
    favorites_action = request.POST.get('favorites_action')
    word_id = kwargs['word_id']
    user_id = request.user.pk

    # Измени статус слова по отношению к избранным.
    if favorites_action == 'add':
        add_word_to_favorites(user_id, word_id)
    elif favorites_action == 'remove':
        remove_word_from_favorites(user_id, word_id)

    # Редирект на формирование нового задания.
    kwargs = {'task_status': 'question'}
    return redirect(reverse_lazy('eng:repetition', kwargs=kwargs))
