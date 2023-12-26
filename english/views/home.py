from django.views.generic import TemplateView


class HomeEnglishView(TemplateView):
    """
    Home page for the subject "English".

    Navigation on the page through theoretical material and tasks
    is transmitted using dictionaries.
    The dictionary contains the name of the item and a link to it.
    """

    users_chapters = {
        'Словарь': 'eng:word_list',
    }
    admin_chapters = {
        'Добавить слово': 'eng:word_create',
    }
    solutions = {
        'Повторить слова': 'eng:start_repetition',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = self.users_chapters
        context['solutions'] = self.solutions
        if self.request.user.is_superuser:
            context['chapters'].update(self.admin_chapters)
        return context
