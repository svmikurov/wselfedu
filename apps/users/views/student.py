"""Defines views to student study management by mentor."""

from typing import Any

from dependency_injector.wiring import Provide, inject
from django.views.generic import DetailView

from di import MainContainer

from ..models import Mentorship
from ..presenters.iabc import IStudentExercisesPresenter


class StudentManagementView(DetailView):  # type: ignore[type-arg]
    """Student study management view."""

    model = Mentorship
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
        context = super().get_context_data()
        context['exercises'] = presenter.get_assigned(self.get_object())
        return context
