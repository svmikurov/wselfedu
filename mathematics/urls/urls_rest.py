"""Mathematics app REST urls."""

from django.urls import path

from mathematics.views.rest.exercise import multiplication_exercise_view

app_name = 'mathematics_rest'

urlpatterns = [
    path(
        'multiplication/',
        multiplication_exercise_view,
        name='multiplication',
    ),
]
