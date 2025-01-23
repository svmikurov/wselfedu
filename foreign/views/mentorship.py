"""Mentors views module."""

import logging

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView

from config.constants import PAGINATE_NUMBER
from foreign.models import Word
from foreign.models.word import AssignedWord


class WordToStudentView(ListView):
    """Add a word by a mentor for a student to study, the view."""

    template_name = 'foreign/mentorship/assign_word_to_student.html'
    model = Word
    context_object_name = 'words'
    paginate_by = PAGINATE_NUMBER

    def get_context_data(self, **kwargs: object) -> dict:
        """Add student id to context."""
        student_id = self.request.resolver_match.kwargs.get('student_id')
        kwargs['student_id'] = student_id
        return super().get_context_data(**kwargs)

    def post(
        self, request: HttpRequest, *args: object, **kwargs: object
    ) -> HttpResponse:
        """Handle the POST: save word assignment."""
        student_id = self.request.resolver_match.kwargs.get('student_id')
        list_of_inputs = request.POST.getlist('selected_option')

        student = AssignedWord.objects.get(student=student_id)
        student.word.set(list_of_inputs)

        logging.info(f'>>> {list_of_inputs = }')

        return redirect(
            reverse(
                'foreign:word_to_student2', kwargs={'student_id': student_id}
            )
        )


class WordToStudentView2(ListView):
    """Add a word by a mentor for a student to study, the view."""

    template_name = 'foreign/mentorship/assign_word_to_student2.html'
    model = AssignedWord
    context_object_name = 'words'
    paginate_by = PAGINATE_NUMBER

    def get_context_data(self, **kwargs: object) -> dict:
        """Add student id."""
        student_id = self.request.resolver_match.kwargs.get('student_id')
        kwargs['student_id'] = student_id
        return super().get_context_data(**kwargs)

    def get_queryset(self) -> QuerySet:
        """Return all assigned to student words."""
        student_id = self.request.resolver_match.kwargs.get('student_id')
        return AssignedWord.objects.get(student=student_id).word.all()
