from django.views.generic import TemplateView


class HomeEnglishView(TemplateView):
    """
    Home page for the subject "English".
    Navigation on the page through theoretical material and tasks
    is transmitted using dictionaries.
    The dictionary contains the name of the item and a link to it.
    """

    # Theoretical Chapters
    chapters = {
        'Словарь': 'eng:word_list',
    }

    # Solutions
    solutions = {
        'Повторить слова': 'eng:start_repetition',
        # 'Тест': '#',
    }

    extra_context = {
        'title': 'Английский язык',
        'chapters': chapters,
        'solutions': solutions,
    }

    def add_for_admin(self, request, kwargs):
        """Enable chapters if user is an admin"""
        if request.user.is_superuser:
            self.chapters.update(
                {
                    'Добавить слово': 'eng:word_create',
                }
            )
