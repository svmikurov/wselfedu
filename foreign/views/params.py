"""Learning foreign words exercise parameters."""

from django.db.models import Model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from config.constants import HOME, PK
from foreign.models import WordParams


class ForeignTaskSettingsView(DetailView):
    """Display user's learning foreign words exercise settings view."""

    model = WordParams
    template_name = 'foreign/params/task_settings.html'

    def get_object(self, **kwargs: object) -> Model:
        """Return the object the view is displaying."""
        pk = self.kwargs.get(PK)
        obj = WordParams.objects.get(user=pk)
        return obj


class CreateForeignTaskSettingsView(CreateView):
    """Create Foreign task settings view."""

    model = WordParams
    template_name = 'foreign/params/create_task_settings.html'
    fields = '__all__'
    success_url = reverse_lazy(HOME)


class UpdateForeignTaskSettingsView(UpdateView):
    """Update Foreign task settings view."""

    model = WordParams
    template_name = 'foreign/params/update_task_settings.html'
    fields = '__all__'
    success_url = reverse_lazy(HOME)
