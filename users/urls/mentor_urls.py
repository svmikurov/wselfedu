"""Mentor urls."""

from django.urls import path

from users import views

mentor_urls = [
    # --======= Mentorship =======--
    # Request to mentor name input page form.
    path(
        'send-mentorship-request/',
        views.InputMentorView.as_view(),
        name='send_mentorship_request',
    ),
    # Request from mentor name input page form.
    path(
        'send-mentorship-request/<int:user_pk>/',
        views.send_mentorship_request,
        name='send_mentorship_request',
    ),
    path(
        'accept-mentorship-request/<int:request_pk>/',
        views.accept_mentorship_request,
        name='accept_mentorship_request',
    ),
    path(
        'delete-mentorship-request/<int:pk>/',
        views.DeleteMentorshipRequestView.as_view(),
        name='delete_mentorship_request',
    ),
    path(
        'delete-mentorship/<int:pk>/',
        views.DeleteMentorshipView.as_view(),
        name='delete_mentorship',
    ),
    # -- EndMentorship --
    # --======= Mentor management =======--
    path(
        'add-exercise/<int:student_id>/',
        views.AddExerciseDataView.as_view(),
        name='add_exercise',
    ),
    # -- End Mentor management --
]
