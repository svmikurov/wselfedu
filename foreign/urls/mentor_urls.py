"""Mentor urls module."""

from django.urls import path

from foreign import views

mentor_paths = [
    path(
        'mentor-adds-words-for-student-study',
        views.AddWordByMentorToStudentView.as_view(),
        name='mentor_adds_words_for_student_study',
    ),
]
