from typing import Dict

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from english.services import (
    update_word_favorites_status,
    update_word_knowledge_assessment,
    get_knowledge_assessment,
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
def update_words_favorites_status_view_ajax(
        request: HttpRequest,
        **kwargs: Dict[str, object],
) -> HttpResponse:
    """Update the status of a word, is it favorite.

    This view receives a request from Ajax when the user wants to
    update the status of a word.

    Parameters
    ----------
    request : `HttpRequest`
        Http request.
    kwargs : `Dict[str, object]`
        The keyword argument that contains the ``word_id`` of the word
        whose status should be updated.

    Return
    ------
    response : `JsonResponse`
        Response with current favorite word status.
    """
    word_id = kwargs['word_id']
    user_id = request.user.pk
    favorites_status = update_word_favorites_status(word_id, user_id)

    # this view gets a request from Ajax
    response = JsonResponse(
        data={
            'favorites_status': favorites_status,
        },
        status=201,
    )
    return response
