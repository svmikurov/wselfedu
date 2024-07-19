from typing import Dict

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from english.services import (
    update_word_favorites_status,
    update_word_knowledge_assessment,
    get_knowledge_assessment,
)


@login_required
def update_word_knowledge_assessment_view(
        request: HttpRequest,
        **kwargs: object,
) -> JsonResponse:
    """Update user word knowledge assessment view.

    Parameters
    ----------
    request : `HttpRequest`
        Request to update user word knowledge assessment.
    **kwargs : `object`
        - ``word_id``: ID of the word whose rating will be updated
          (`str`).

    Returns
    -------
    `JsonResponse`
        Response with status 201.
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
) -> JsonResponse:
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
