"""Defines Users app web paths."""

from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'profile/<int:pk>/',
        views.ProfileView.as_view(),
        name='profile',
    ),
    # Exercise assignation
    path(
        'mentorship/<int:pk>/student/',
        views.AssignedExercisesView.as_view(),
        name='mentorship-mentor-student',
    ),
    path(
        'mentorship/<int:pk>/student/assign/',
        views.AssignExerciseView.as_view(),
        name='mentorship-mentor-student-assign',
    ),
    # Mentorship management
    path(
        'mentorship/<int:pk>/',
        views.MentorshipView.as_view(),
        name='mentorship',
    ),
    path(
        'mentorship/mentor/delete/<int:pk>/',
        views.DeleteStudentView.as_view(),
        name='mentorship-mentor-delete',
    ),
    path(
        'mentorship/mentor/accept-request/<int:pk>/',
        views.AcceptMentorshipRequest.as_view(),
        name='mentorship-mentor-request-accept',
    ),
    path(
        'mentorship/mentor/delete-request/<int:pk>/',
        views.DeleteStudentRequestView.as_view(),
        name='mentorship-mentor-request-delete',
    ),
    path(
        'mentorship/student/delete/<int:pk>/',
        views.DeleteMentorView.as_view(),
        name='mentorship-student-delete',
    ),
    path(
        'mentorship/student/delete-request/<int:pk>/',
        views.DeleteMentorRequestView.as_view(),
        name='mentorship-student-request-delete',
    ),
]
