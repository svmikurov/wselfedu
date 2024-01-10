from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from english.models import WordUserKnowledgeRelation, WordModel
from english.services import remove_word_from_favorites, add_word_to_favorites
from users.models import UserModel


@require_POST
@login_required
def change_words_knowledge_assessment_view(request, **kwargs):
    """Изменяет в модели WordUserKnowledgeRelation значение поля
       knowledge_assessment (самооценки пользователем знания слова).
    """
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


@require_POST
@login_required
def change_words_favorites_status_view(request, **kwargs):
    """Если слова нет среди избранных - добавляет слова в избранные,
       если слово среди избранных - убирает из избранных.
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
