"""Curriculum view."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class ExercisesForTodayView(
    LoginRequiredMixin,
    generic.TemplateView,
):
    """Exercise page for today study."""

    template_name = 'lang/tasks/index.html'
