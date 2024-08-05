"""Mentor actions views module."""

from django.urls import reverse_lazy
from django.views.generic import RedirectView


class AddWordByMentorToStudentViewRedirect(RedirectView):
    """Redirect to AddWordByMentorToStudentView
    with data in session view."""

    url = reverse_lazy('english:mentor_adds_words_for_student_study')
    """Url to redirect.
    """

    def get(self, request, *args, **kwargs):
        """Add student id to session."""
        request.session['student'] = kwargs.get('student')
        response = super().get(request, *args, **kwargs)
        return response
