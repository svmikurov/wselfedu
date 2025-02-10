"""Mathematics app REST urls."""

from django.urls import path

from mathematics.views.rest.exercise import (
    handle_answer_view,
    render_task_view,
)

app_name = 'mathematics_rest'

urlpatterns = [
    path(
        'calculations/',
        render_task_view,
        name='calculations',
    ),
    path(
        'handel-answer/',
        handle_answer_view,
        name='handel_answer',
    ),
]
