"""Learning foreign words task settings module."""

from django.db.models import Model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from config.constants import HOME, PK
from task.models import ForeignExerciseSettings


class ForeignTaskSettingsView(DetailView):
    """Display user's learning foreign words exercise settings view."""

    model = ForeignExerciseSettings
    template_name = 'foreign/tasks/task_settings.html'

    def get_object(self, **kwargs: object) -> Model:
        """Return the object the view is displaying."""
        pk = self.kwargs.get(PK)
        obj = ForeignExerciseSettings.objects.get(user=pk)
        return obj


class CreateForeignTaskSettingsView(CreateView):
    """Create Foreign task settings view."""

    model = ForeignExerciseSettings
    template_name = 'foreign/tasks/create_task_settings.html'
    fields = '__all__'
    success_url = reverse_lazy(HOME)


class UpdateForeignTaskSettingsView(UpdateView):
    """Update Foreign task settings view."""

    model = ForeignExerciseSettings
    template_name = 'foreign/tasks/update_task_settings.html'
    fields = '__all__'
    success_url = reverse_lazy(HOME)
