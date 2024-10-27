"""Mentors views module."""

from django.forms import Form
from django.http import HttpResponse
from django.views.generic import CreateView

from foreign.views import WordCreateView


class AddWordByMentorToStudentView(WordCreateView):
    """Add a word by a mentor for a student to study view."""

    def form_valid(self, form: Form) -> HttpResponse:
        """Add mentor and student to form."""
        form.instance.user = self.request.session['student']
        form.instance.mentor = self.request.user
        form.save()
        response = super(CreateView).form_valid(form)
        return response
