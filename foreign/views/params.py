"""Learning foreign words exercise parameters."""

from django.db.models import Model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from foreign.models import TranslateParams


class ForeignTaskSettingsView(DetailView):
    """Display user's learning foreign words exercise settings view."""

    model = TranslateParams
    template_name = 'foreign/params/task_settings.html'

    def get_object(self, **kwargs: object) -> Model:
        """Return the object the view is displaying."""
        pk = self.kwargs.get('pk')
        obj = TranslateParams.objects.get(user=pk)
        return obj


class CreateForeignTaskSettingsView(CreateView):
    """Create Foreign task settings view."""

    model = TranslateParams
    template_name = 'foreign/params/create_task_settings.html'
    fields = '__all__'
    success_url = reverse_lazy('home')


class UpdateForeignTaskSettingsView(UpdateView):
    """Update Foreign task settings view."""

    model = TranslateParams
    template_name = 'foreign/params/update_task_settings.html'
    fields = '__all__'
    success_url = reverse_lazy('home')
