"""Mentor urls module."""

from django.urls import path

from english import views

mentor_urls = [
    path(
        'mentor-adds-words-for-student-study',
        views.AddWordByMentorToStudentView.as_view(),
        name='mentor_adds_words_for_student_study',
    ),
]
