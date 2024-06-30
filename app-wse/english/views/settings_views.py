from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView

from task.models import EnglishTaskSettings


class EnglishTaskSettingsView(DetailView):
    """Display user's english task settings view."""

    model = EnglishTaskSettings
    template_name = 'english/tasks/task_settings.html'

    def get_object(self, **kwargs):
        """"""
        pk = self.kwargs.get('pk')
        obj = EnglishTaskSettings.objects.get(user=pk)
        print(f'{obj = }')
        return obj


class CreateEnglishTaskSettingsView(CreateView):
    model = EnglishTaskSettings
    template_name = 'english/tasks/create_task_settings.html'
    fields = '__all__'
    success_url = reverse_lazy('home')


class UpdateEnglishTaskSettingsView(UpdateView):
    model = EnglishTaskSettings
    template_name = 'english/tasks/update_task_settings.html'
    fields = '__all__'
    success_url = reverse_lazy('home')
