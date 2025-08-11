"""Defines views to student study management by mentor."""

from functools import cached_property
from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import DetailView, FormView, View
from django.views.generic.edit import FormMixin

from di import MainContainer

from ...core.orchestrators.exercise import ExerciseAssignator
from ..forms.assignation import AssignExerciseForm
from ..models import Mentorship
from ..presenters.iabc import IStudentExercisesPresenter


class AssignedExercisesView(
    LoginRequiredMixin,
    FormMixin,  # type: ignore[type-arg]
    DetailView,  # type: ignore[type-arg]
):
    """Detail exercise assignation view."""

    model = Mentorship
    form_class = AssignExerciseForm
    template_name = 'users/mentor/student.html'

    @inject
    def get_context_data(
        self,
        presenter: IStudentExercisesPresenter = Provide[
            MainContainer.users_container.exercises_presenter,
        ],
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Add data to context."""
        assigned_exercises = presenter.get_assigned_exercise(self.get_object())
        context = super().get_context_data(**kwargs)
        context['assigned_exercises'] = assigned_exercises
        return context

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add mentorship instance to form."""
        kwargs = super().get_form_kwargs()
        kwargs['mentorship'] = self.get_object()
        return kwargs


class AssignExerciseView(
    LoginRequiredMixin,
    FormView,  # type: ignore[type-arg]
):
    """Assign exercise to user by mentor."""

    model = Mentorship
    form_class = AssignExerciseForm
    partial_template = 'users/mentor/table_student_exercises.html'
    template_name = 'users/mentor/student.html'

    def form_valid(self, form: AssignExerciseForm) -> HttpResponse:
        """Create exercise assignation."""
        try:
            form.create()
        except Exception as e:
            form.add_error(None, str(e))
            html = self._get_html(form=form)
        else:
            html = self._get_html(
                form=AssignExerciseForm(mentorship=self.get_object())
            )

        return HttpResponse(html)

    def form_invalid(self, form: AssignExerciseForm) -> HttpResponse:
        """If the form is invalid, render the invalid form."""
        if 'Hx-Request' in self.request.headers:
            return HttpResponse(self._get_html(form=form))
        return super().form_invalid(form)

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add mentorship instance to form."""
        kwargs = super().get_form_kwargs()
        kwargs['mentorship'] = self.get_object()
        return kwargs

    @inject
    def _get_html(
        self,
        form: AssignExerciseForm,
        presenter: IStudentExercisesPresenter = Provide[
            MainContainer.users_container.exercises_presenter
        ],
    ) -> str:
        """Get HTML to render on request HTMX."""
        assigned_exercises = presenter.get_assigned_exercise(self.get_object())
        render = render_to_string(
            self.partial_template,
            {
                'assigned_exercises': assigned_exercises,
                'form': form,
                'object': self.get_object(),
            },
            request=self.request,
        )
        return render

    def get_object(self) -> Mentorship:
        """Get mentorship instance."""
        return get_object_or_404(
            Mentorship,
            pk=self.kwargs['pk'],
            mentor=self.request.user,
        )


class DeleteAssignationView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    View,
):
    """Delete the assignation."""

    def delete(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponse:
        """Delete the exercise assignation."""
        ExerciseAssignator.delete(self.kwargs['exercise_id'])
        return HttpResponse(status=HTTPStatus.OK)

    def test_func(self) -> bool:
        """Test on request ownership."""
        return bool(self.request.user == self.mentorship.mentor)

    @cached_property
    def mentorship(self) -> Mentorship:
        """Get mentorship instance."""
        return get_object_or_404(Mentorship, pk=self.kwargs['mentorship_id'])
