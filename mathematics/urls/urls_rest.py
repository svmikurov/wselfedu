"""Mathematics app REST urls."""

from django.urls import path

from mathematics.views_rest.exercise import (
    handle_answer,
    render_task,
)

app_name = 'mathematics_rest'

urlpatterns = [
    path(
        'calculations/',
        render_task,
        name='calculations',
    ),
    path(
        'handel-answer/',
        handle_answer,
        name='handel_answer',
    ),
]
