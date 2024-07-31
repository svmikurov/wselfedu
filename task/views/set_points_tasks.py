"""This module contains views with initial data for exercises.
"""
from django.http import HttpRequest, HttpResponseBase
from django.urls import reverse_lazy
from django.views.generic import RedirectView


class SetMultiplicationTableExerciseView(RedirectView):
    """Setup initial data for multiplication table exercises view."""

    url = reverse_lazy('task:math_calculate_solution')

    def get(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponseBase:
        """Save task conditions in session."""
        task_conditions = {
            'calculation_type': 'mul',
            'min_value': 2,
            'max_value': 9,
        }
        request.session['task_conditions'] = task_conditions
        response = super().get(request, *args, **kwargs)
        return response
